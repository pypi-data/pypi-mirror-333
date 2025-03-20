import io
import json
import logging
import os
import re
import shutil
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Generator, Optional

import pkg_resources
import requests

from preswald.utils import get_project_slug, read_template


logger = logging.getLogger(__name__)

# Default Structured Cloud service URL
# STRUCTURED_CLOUD_SERVICE_URL = os.getenv('STRUCTURED_CLOUD_SERVICE_URL', 'http://127.0.0.1:8080')
STRUCTURED_CLOUD_SERVICE_URL = "https://deployer.preswald.com"


def get_deploy_dir(script_path: str) -> Path:
    """
    Creates and returns a persistent deployment directory next to the script.
    This directory will store all deployment-related files.
    """
    script_dir = Path(script_path).parent
    deploy_dir = script_dir / ".preswald_deploy"
    deploy_dir.mkdir(exist_ok=True)
    return deploy_dir


def get_container_name(script_path: str) -> str:
    """Generate a consistent container name for a given script"""
    container_name = f"preswald-app-{Path(script_path).stem}"
    container_name = container_name.lower()
    container_name = re.sub(r"[^a-z0-9-]", "", container_name)
    container_name = container_name.strip("-")
    return container_name


def stop_existing_container(container_name: str) -> None:
    """Stop and remove any existing container with the same name"""
    try:
        # Stop the container if it's running
        subprocess.run(
            ["docker", "stop", container_name],
            check=False,  # Don't raise error if container doesn't exist
            capture_output=True,
        )
        # Remove the container
        subprocess.run(
            ["docker", "rm", container_name], check=False, capture_output=True
        )
    except Exception as e:
        logger.warning(f"Error cleaning up container: {e}")


def check_gcloud_installation() -> bool:
    """
    Check if the Google Cloud SDK is installed and accessible.
    Returns True if gcloud is installed, False otherwise.
    """
    try:
        subprocess.run(["gcloud", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_gcloud_auth() -> bool:
    """
    Check if the user is authenticated with Google Cloud.
    Returns True if authenticated, False otherwise.
    """
    try:
        # Try to get the current account
        result = subprocess.run(
            ["gcloud", "auth", "list", "--format=value(account)"],
            check=True,
            capture_output=True,
            text=True,
        )
        return bool(result.stdout.strip())
    except subprocess.CalledProcessError:
        return False


def setup_gcloud() -> None:
    """
    Guide the user through setting up Google Cloud SDK and authentication.
    Raises an exception if setup fails.
    """
    if not check_gcloud_installation():
        print(
            "\nGoogle Cloud SDK not found. You'll need to install it to deploy to Cloud Run."
        )
        print("\nInstallation instructions:")
        print("1. Visit https://cloud.google.com/sdk/docs/install")
        print("2. Follow the installation steps for your operating system")
        print("3. Run this deployment command again")
        raise Exception("Please install Google Cloud SDK first")

    if not check_gcloud_auth():
        print("\nYou need to authenticate with Google Cloud.")
        print("Opening browser for authentication...")

        try:
            # Run authentication command
            subprocess.run(["gcloud", "auth", "login"], check=True)

            # Configure Docker auth
            print("\nConfiguring Docker authentication...")
            subprocess.run(["gcloud", "auth", "configure-docker"], check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Authentication failed: {e!s}") from e


def ensure_project_selected() -> str:
    """
    Ensure a Google Cloud project is selected.
    Returns the project ID.
    """
    try:
        project_id = subprocess.check_output(
            ["gcloud", "config", "get-value", "project"], text=True
        ).strip()

        if not project_id:
            print("\nNo Google Cloud project selected.")
            print("Available projects:")

            # List available projects
            subprocess.run(["gcloud", "projects", "list"], check=True)

            # Prompt for project ID
            project_id = input("\nEnter the project ID you want to use: ").strip()

            # Set the project
            subprocess.run(
                ["gcloud", "config", "set", "project", project_id], check=True
            )

        return project_id

    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to get or set project: {e!s}") from e


def deploy_to_cloud_run(deploy_dir: Path, container_name: str, port: int = 8501) -> str:
    """
    Deploy a Preswald app to Google Cloud Run.

    Args:
        deploy_dir: Path to the deployment directory containing the Docker context
        container_name: Name to use for the container

    Returns:
        str: The URL where the app is deployed
    """
    try:
        # First, ensure Google Cloud SDK is set up properly
        setup_gcloud()

        # Ensure a project is selected
        project_id = ensure_project_selected()

        region = "us-west1"  # Default region, could be made configurable
        gcr_image = f"gcr.io/{project_id}/{container_name}"

        print("Pushing image to Google Container Registry...")

        # Tag and push the image
        subprocess.run(
            ["docker", "tag", container_name, gcr_image], check=True, cwd=deploy_dir
        )
        subprocess.run(["docker", "push", gcr_image], check=True, cwd=deploy_dir)

        print("Deploying to Cloud Run...")

        # Deploy to Cloud Run
        subprocess.run(
            [
                "gcloud",
                "run",
                "deploy",
                container_name,
                "--image",
                gcr_image,
                "--platform",
                "managed",
                "--region",
                region,
                "--allow-unauthenticated",  # Makes the service publicly accessible
                "--port",
                f"{port}",  # Match the port your app uses
            ],
            check=True,
            text=True,
            capture_output=True,
        )

        url_result = subprocess.run(
            [
                "gcloud",
                "run",
                "services",
                "describe",
                container_name,  # Same name used in deployment
                "--platform",
                "managed",
                "--region",
                region,
                "--format=value(status.url)",
            ],
            check=True,
            text=True,
            capture_output=True,
        )

        return url_result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if "not installed" in str(e):
            raise Exception(
                "Google Cloud SDK not found. Please install from: "
                "https://cloud.google.com/sdk/docs/install"
            ) from e
        raise Exception(f"Cloud Run deployment failed: {e!s}") from e
    except Exception as e:
        raise Exception(f"Deployment failed: {e!s}") from e


def deploy_to_prod(  # noqa: C901
    script_path: str,
    port: int = 8501,
    github_username: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Generator[dict, None, None]:
    """
    Deploy a Preswald app to production via Structured Cloud service.

    Args:
        script_path: Path to the Preswald application script
        port: Port number for the deployment
        github_username: Optional GitHub username provided via CLI
        api_key: Optional Structured Cloud API key provided via CLI

    Returns:
        Generator yielding deployment status updates
    """
    script_path = os.path.abspath(script_path)
    script_dir = Path(script_path).parent
    config_path = script_dir / "preswald.toml"
    env_file = script_dir / ".env.structured"

    # Get project slug from preswald.toml
    try:
        project_slug = get_project_slug(config_path)
    except Exception as e:
        yield {
            "status": "error",
            "message": f"Failed to get project slug: {e!s}",
            "timestamp": datetime.now().isoformat(),
        }
        raise Exception(f"Failed to get project slug: {e!s}") from e

    if not env_file.exists():
        # Use provided credentials or get from user input
        if not github_username:
            github_username = input("Enter your GitHub username: ")
        if not api_key:
            structured_cloud_api_key = input("Enter your Structured Cloud API key: ")
        else:
            structured_cloud_api_key = api_key

        # Create and populate .env.structured file
        with open(env_file, "w") as f:
            f.write(f"GITHUB_USERNAME={github_username}\n")
            f.write(f"STRUCTURED_CLOUD_API_KEY={structured_cloud_api_key}\n")
    else:
        # Read credentials from existing env file if not provided via CLI
        credentials = {}
        with open(env_file) as f:
            for line in f:
                key, value = line.strip().split("=")
                credentials[key] = value

        github_username = github_username or credentials["GITHUB_USERNAME"]
        structured_cloud_api_key = api_key or credentials["STRUCTURED_CLOUD_API_KEY"]

    # Create a temporary zip file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Walk through the script directory and add all files
        for root, _, files in os.walk(script_dir):
            for file in files:
                # Skip .preswald_deploy directory
                if ".preswald_deploy" in root:
                    continue

                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, script_dir)
                zip_file.write(file_path, arc_name)

    # Prepare the zip file for sending
    zip_buffer.seek(0)
    files = {"deployment": ("app.zip", zip_buffer, "application/zip")}

    try:
        git_repo_name = (
            subprocess.check_output(
                ["git", "config", "--get", "remote.origin.url"], cwd=script_dir
            )
            .decode("utf-8")
            .strip()
        )

        git_repo_name = git_repo_name.split("/")[-1].replace(".git", "")
    except subprocess.CalledProcessError:
        git_repo_name = os.path.basename(script_dir)

    try:
        response = requests.post(
            f"{STRUCTURED_CLOUD_SERVICE_URL}/deploy",
            files=files,
            data={
                "github_username": github_username,
                "structured_cloud_api_key": structured_cloud_api_key,
                "project_slug": project_slug,
                "git_repo_name": git_repo_name,
            },
            stream=True,
        )
        response.raise_for_status()

        # Process SSE stream
        for line in response.iter_lines():
            if line:
                # SSE lines start with "data: "
                if line.startswith(b"data: "):
                    data = json.loads(line[6:].decode("utf-8"))
                    yield data

    except requests.RequestException as e:
        yield {
            "status": "error",
            "message": f"Deployment failed: {e!s}",
            "timestamp": datetime.now().isoformat(),
        }
        raise Exception(f"Production deployment failed: {e!s}") from e


def deploy_to_gcp(script_path: str, port: int = 8501) -> str:
    """
    Deploy a Preswald app to Google Cloud Run.
    This function creates a Docker container locally and deploys it to Cloud Run.

    Args:
        script_path: Path to the Preswald application script
        port: Port number for the deployment

    Returns:
        str: The URL where the application is deployed on Cloud Run
    """
    script_path = os.path.abspath(script_path)
    script_dir = Path(script_path).parent
    container_name = get_container_name(script_path)
    deploy_dir = get_deploy_dir(script_path)

    # Get preswald version for exact version matching
    preswald_version = pkg_resources.get_distribution("preswald").version

    # Clear out old deployment directory contents while preserving the directory itself
    for item in deploy_dir.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)

    # Copy everything from script's directory to deployment directory
    for item in script_dir.iterdir():
        if item.name == ".preswald_deploy":
            continue
        if item.is_file():
            shutil.copy2(item, deploy_dir / item.name)
        elif item.is_dir():
            shutil.copytree(item, deploy_dir / item.name)

    # Rename main script to app.py if needed
    if Path(script_path).name != "app.py":
        shutil.move(deploy_dir / Path(script_path).name, deploy_dir / "app.py")

    # Create startup script
    startup_template = read_template("run.py")
    startup_script = startup_template.format(port=port)
    with open(deploy_dir / "run.py", "w") as f:
        f.write(startup_script)

    # Create Dockerfile
    dockerfile_template = read_template("Dockerfile")
    dockerfile_content = dockerfile_template.format(
        port=port, preswald_version=preswald_version
    )
    with open(deploy_dir / "Dockerfile", "w") as f:
        f.write(dockerfile_content)

    # Store deployment info
    deployment_info = {
        "script": script_path,
        "container_name": container_name,
        "preswald_version": preswald_version,
    }
    with open(deploy_dir / "deployment.json", "w") as f:
        json.dump(deployment_info, f, indent=2)

    try:
        # Stop any existing container
        print("Stopping existing deployment (if any)...")
        stop_existing_container(container_name)

        # Build the Docker image for GCP (using linux/amd64 platform)
        print(f"Building Docker image {container_name} for GCP deployment...")
        subprocess.run(
            [
                "docker",
                "build",
                "--platform",
                "linux/amd64",
                "-t",
                container_name,
                ".",
            ],
            check=True,
            cwd=deploy_dir,
        )

        # Deploy to Cloud Run
        return deploy_to_cloud_run(deploy_dir, container_name, port=port)

    except subprocess.CalledProcessError as e:
        raise Exception(f"Docker operation failed: {e!s}") from e
    except FileNotFoundError as e:
        raise Exception(
            "Docker not found. Please install Docker Desktop from "
            "https://www.docker.com/products/docker-desktop"
        ) from e


def deploy(  # noqa: C901
    script_path: str,
    target: str = "local",
    port: int = 8501,
    github_username: Optional[str] = None,
    api_key: Optional[str] = None,
) -> str | Generator[dict, None, None]:
    """
    Deploy a Preswald app.

    Args:
        script_path: Path to the Preswald application script
        target: Deployment target ("local", "gcp", "aws", or "prod")
        port: Port number for the deployment
        github_username: Optional GitHub username for structured deployment
        api_key: Optional Structured Cloud API key for structured deployment

    Returns:
        str | Generator: URL where the application can be accessed for local/cloud deployments,
                        or a Generator yielding deployment status for production deployments
    """
    if target == "structured":
        return deploy_to_prod(script_path, port, github_username, api_key)
    elif target == "gcp":
        return deploy_to_gcp(script_path, port)
    elif target == "local":
        script_path = os.path.abspath(script_path)
        script_dir = Path(script_path).parent
        container_name = get_container_name(script_path)
        deploy_dir = get_deploy_dir(script_path)
        # Get preswald version for exact version matching
        preswald_version = pkg_resources.get_distribution("preswald").version
        # First, clear out the old deployment directory contents while preserving the directory itself
        for item in deploy_dir.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        # Copy everything from the script's directory to the deployment directory
        for item in script_dir.iterdir():
            # Skip the deployment directory itself to avoid recursive copying
            if item.name == ".preswald_deploy":
                continue
            # Copy files and directories
            if item.is_file():
                shutil.copy2(item, deploy_dir / item.name)
            elif item.is_dir():
                shutil.copytree(item, deploy_dir / item.name)
        # Rename the main script to app.py if it's not already named that
        if Path(script_path).name != "app.py":
            shutil.move(deploy_dir / Path(script_path).name, deploy_dir / "app.py")
        # Create startup script
        startup_template = read_template("run.py")
        startup_script = startup_template.format(port=port)
        with open(deploy_dir / "run.py", "w") as f:
            f.write(startup_script)
        # Create Dockerfile
        dockerfile_template = read_template("Dockerfile")
        dockerfile_content = dockerfile_template.format(
            port=port, preswald_version=preswald_version
        )
        with open(deploy_dir / "Dockerfile", "w") as f:
            f.write(dockerfile_content)
        # Store deployment info
        deployment_info = {
            "script": script_path,
            "container_name": container_name,
            "preswald_version": preswald_version,
        }
        with open(deploy_dir / "deployment.json", "w") as f:
            json.dump(deployment_info, f, indent=2)
        try:
            # Stop any existing container
            print("Stopping existing deployment (if any)...")
            stop_existing_container(container_name)
            # Build the Docker image
            print(f"Building Docker image {container_name}...")
            subprocess.run(
                ["docker", "build", "-t", container_name, "."],
                check=True,
                cwd=deploy_dir,
            )
            # Start the container
            print("Starting container...")
            subprocess.run(
                [
                    "docker",
                    "run",
                    "-d",
                    "--name",
                    container_name,
                    "-p",
                    f"{port}:{port}",
                    container_name,
                ],
                check=True,
                cwd=deploy_dir,
            )
            return f"http://localhost:{port}"
        except subprocess.CalledProcessError as e:
            raise Exception(f"Docker operation failed: {e!s}") from e
        except FileNotFoundError as e:
            raise Exception(
                "Docker not found. Please install Docker Desktop from "
                "https://www.docker.com/products/docker-desktop"
            ) from e
    else:
        raise ValueError(f"Unsupported deployment target: {target}")


def stop(current_dir: Optional[str] = None) -> None:
    """
    Stop a running Preswald deployment.

    If script_path is provided, stops that specific deployment.
    Otherwise, looks for a deployment in the current directory.
    """
    if current_dir:
        deploy_dir = Path(current_dir) / ".preswald_deploy"
    else:
        # Look for deployment in current directory
        deploy_dir = Path.cwd() / ".preswald_deploy"

    if not deploy_dir.exists():
        raise Exception("No deployment found")

    try:
        with open(deploy_dir / "deployment.json") as f:
            info = json.load(f)
            container_name = info["container_name"]

        print(f"Stopping deployment {container_name}...")
        stop_existing_container(container_name)

    except Exception as e:
        raise Exception(f"Failed to stop deployment: {e}") from e


def stop_structured_deployment(script_dir: str) -> dict:
    """
    Stop a Preswald app deployed to Structured Cloud service.

    Args:
        script_path: Path to the Preswald application script

    Returns:
        dict: Status of the stop operation
    """
    config_path = Path(script_dir) / "preswald.toml"
    env_file = Path(script_dir) / ".env.structured"

    # Get project slug from preswald.toml
    try:
        project_slug = get_project_slug(config_path)
    except Exception as e:
        raise Exception(f"Failed to get project slug: {e!s}") from e

    if not env_file.exists():
        raise Exception("No deployment found. The .env.structured file is missing.")

    # Read credentials from existing env file
    credentials = {}
    with open(env_file) as f:
        for line in f:
            key, value = line.strip().split("=")
            credentials[key] = value

    github_username = credentials["GITHUB_USERNAME"]
    structured_cloud_api_key = credentials["STRUCTURED_CLOUD_API_KEY"]

    try:
        response = requests.post(
            f"{STRUCTURED_CLOUD_SERVICE_URL}/stop",
            json={
                "github_username": github_username,
                "structured_cloud_api_key": structured_cloud_api_key,
                "project_slug": project_slug,
            },
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        raise Exception(f"Failed to stop production deployment: {e!s}") from e


def get_structured_deployments(script_path: str) -> dict:
    """
    Get deployments from Structured Cloud service.

    Args:
        script_path: Path to the Preswald application script

    Returns:
        dict: Deployment information including user, organization, and deployments list
    """
    script_dir = Path(script_path).parent
    config_path = script_dir / "preswald.toml"
    env_file = script_dir / ".env.structured"

    # Get project slug from preswald.toml
    try:
        project_slug = get_project_slug(config_path)
    except Exception as e:
        raise Exception(f"Failed to get project slug: {e!s}") from e

    if not env_file.exists():
        raise Exception("No deployment found. The .env.structured file is missing.")

    # Read credentials from existing env file
    credentials = {}
    with open(env_file) as f:
        for line in f:
            key, value = line.strip().split("=")
            credentials[key] = value

    github_username = credentials["GITHUB_USERNAME"]
    structured_cloud_api_key = credentials["STRUCTURED_CLOUD_API_KEY"]

    try:
        response = requests.post(
            f"{STRUCTURED_CLOUD_SERVICE_URL}/deployments",
            json={
                "github_username": github_username,
                "structured_cloud_api_key": structured_cloud_api_key,
                "project_slug": project_slug,
            },
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        raise Exception(f"Failed to fetch deployments: {e!s}") from e


def cleanup_gcp_deployment(script_path: str):  # noqa: C901
    import json
    import subprocess
    from datetime import datetime

    def log_status(status, message):
        return {
            "status": status,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
        }

    try:
        yield log_status("info", "Gathering deployment information...")
        script_path = os.path.abspath(script_path)
        # script_dir = Path(script_path).parent
        container_name = get_container_name(script_path)

        yield log_status("info", "Verifying Google Cloud SDK setup...")
        try:
            setup_gcloud()
        except Exception as e:
            yield log_status("error", f"Failed to setup Google Cloud SDK: {e!s}")
            return

        try:
            project_id = ensure_project_selected()
            yield log_status("success", f"Found GCP project: {project_id}")
        except Exception as e:
            yield log_status("error", f"Failed to get GCP project: {e!s}")
            return

        region = "us-west1"
        gcr_image = f"gcr.io/{project_id}/{container_name}"

        yield log_status(
            "info", f"Attempting to delete Cloud Run service: {container_name}"
        )
        try:
            service_check = subprocess.run(
                [
                    "gcloud",
                    "run",
                    "services",
                    "describe",
                    container_name,
                    "--platform",
                    "managed",
                    "--region",
                    region,
                    "--format=json",
                ],
                capture_output=True,
                text=True,
            )

            if service_check.returncode == 0:
                delete_result = subprocess.run(
                    [
                        "gcloud",
                        "run",
                        "services",
                        "delete",
                        container_name,
                        "--platform",
                        "managed",
                        "--region",
                        region,
                        "--quiet",
                    ],
                    capture_output=True,
                    text=True,
                )

                if delete_result.returncode == 0:
                    yield log_status(
                        "success",
                        f"Successfully deleted Cloud Run service: {container_name}",
                    )
                else:
                    yield log_status(
                        "error",
                        f"Failed to delete Cloud Run service: {delete_result.stderr}",
                    )
            else:
                yield log_status(
                    "info", f"No Cloud Run service found with name: {container_name}"
                )
        except Exception as e:
            yield log_status("error", f"Error while deleting Cloud Run service: {e!s}")

        yield log_status("info", f"Cleaning up container images from GCR: {gcr_image}")
        try:
            list_result = subprocess.run(
                [
                    "gcloud",
                    "container",
                    "images",
                    "list-tags",
                    gcr_image,
                    "--format=json",
                ],
                capture_output=True,
                text=True,
            )

            if list_result.returncode == 0:
                images = json.loads(list_result.stdout)
                if images:
                    yield log_status("info", "Removing image tags...")
                    for image in images:
                        tags = image.get("tags", [])
                        for tag in tags:
                            untag_result = subprocess.run(
                                [
                                    "gcloud",
                                    "container",
                                    "images",
                                    "untag",
                                    f"{gcr_image}:{tag}",
                                    "--quiet",
                                ],
                                capture_output=True,
                                text=True,
                            )
                            if untag_result.returncode == 0:
                                yield log_status("success", f"Removed tag: {tag}")
                            else:
                                yield log_status(
                                    "warning",
                                    f"Failed to remove tag {tag}: {untag_result.stderr}",
                                )

                    for image in images:
                        digest = image.get("digest")
                        if digest:
                            delete_image_result = subprocess.run(
                                [
                                    "gcloud",
                                    "container",
                                    "images",
                                    "delete",
                                    f"{gcr_image}@{digest}",
                                    "--force-delete-tags",
                                    "--quiet",
                                ],
                                capture_output=True,
                                text=True,
                            )

                            if delete_image_result.returncode == 0:
                                yield log_status(
                                    "success", f"Deleted container image: {digest[:12]}"
                                )
                            else:
                                yield log_status(
                                    "error",
                                    f"Failed to delete image {digest[:12]}: {delete_image_result.stderr}",
                                )

                    repo_delete_result = subprocess.run(
                        [
                            "gcloud",
                            "container",
                            "images",
                            "delete",
                            gcr_image,
                            "--force-delete-tags",
                            "--quiet",
                        ],
                        capture_output=True,
                        text=True,
                    )

                    if repo_delete_result.returncode == 0:
                        yield log_status(
                            "success", "Successfully deleted container image repository"
                        )
                    else:
                        yield log_status(
                            "error",
                            f"Failed to delete image repository: {repo_delete_result.stderr}",
                        )
                else:
                    yield log_status("info", "No container images found to clean up")
            else:
                yield log_status(
                    "error", f"Failed to list container images: {list_result.stderr}"
                )
        except Exception as e:
            yield log_status(
                "error", f"Error while cleaning up container images: {e!s}"
            )

        yield log_status("info", "Cleaning up local Docker images...")
        try:
            subprocess.run(
                ["docker", "rmi", container_name], capture_output=True, text=True
            )
            subprocess.run(["docker", "rmi", gcr_image], capture_output=True, text=True)
            yield log_status("success", "Cleaned up local Docker images")
        except Exception as e:
            yield log_status(
                "info", f"Note: Could not clean local Docker images: {e!s}"
            )

        yield log_status("success", "GCP cleanup completed successfully!")

    except Exception as e:
        yield log_status("error", f"Unexpected error during cleanup: {e!s}")
        raise
