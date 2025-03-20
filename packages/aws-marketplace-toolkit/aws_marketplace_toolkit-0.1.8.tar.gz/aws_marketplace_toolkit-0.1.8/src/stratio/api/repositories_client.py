# src/stratio/api/repositories_client.py
import base64
import logging
import os
import subprocess
import tarfile
import tempfile
import threading
import zipfile
from typing import Optional

import boto3
import yaml
from botocore.client import BaseClient

from stratio.api import BaseRepositoriesClient
from stratio.api.callbacks import ProgressCallback
from stratio.api.models import Chart, UploadResult
from stratio.api.models.repositories import DeleteResult
from stratio.api.session import ApiSession, CredentialsApiSession, ProfileApiSession
from stratio.config import Config


class Trace:
    INFO = "info"
    WARN = "warn"
    TRACE = "trace"


class RepositoriesClient(BaseRepositoriesClient):
    """
    Client for cluster-related operations.
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        root_session: Optional[ApiSession] = None,
        shared_session: Optional[ApiSession] = None,
        aws_root_session: Optional[boto3.Session] = None,
        aws_shared_session: Optional[boto3.Session] = None,
        config: Optional[Config] = None,
    ):
        super().__init__(logger=logger, root_session=root_session, shared_session=shared_session, config=config)
        self._aws_shared_session = aws_shared_session
        self._aws_root_session = aws_root_session

    def helm_upload_charts(
        self, charts: list[Chart], prefix: str, regions: list[str] = None, progress: Optional[ProgressCallback] = None
    ) -> UploadResult:
        self.logger.info(f"Uploading ({len(charts)}) Helm charts to ECR")

        organization_id, root_ou_id, customers_ou_id = self._get_organizations()
        upload_failures = []
        upload_exists = []
        upload_success = []

        ecr_regions = regions if regions else [self.config.universe.region]

        for ecr_region in ecr_regions:
            ecr_client = self._aws_shared_session.client("ecr", region_name=ecr_region)
            if not self._helm_login(ecr_client):
                raise RuntimeError("Failed to login to ECR with Helm")

            sts_client = self._aws_shared_session.client("sts")
            account_id = sts_client.get_caller_identity()["Account"]
            ecr_url = f"{account_id}.dkr.ecr.{ecr_region}.amazonaws.com"

            total_charts = len(charts)
            self._log_progress(Trace.INFO, f"Uploading {total_charts} charts", 0, total_charts, progress)

            for idx, chart in enumerate(charts, start=1):
                repo_name = f"{prefix}/{chart.name}"

                # apply the necessary permissions to the repository
                self._apply_policy(ecr_client, repo_name, organization_id, root_ou_id, customers_ou_id)

                # skip on error or already uploaded chart
                exists, error = self._chart_exists_in_ecr(ecr_client, repo_name, chart.version)
                if error:
                    upload_failures.append(f"{chart.name}-{chart.version}: {error}")
                    trace = f"Error uploading {chart.name}-{chart.version}: {error}"
                    self._log_progress(Trace.WARN, trace, idx, total_charts, progress)
                    continue

                if exists:
                    upload_exists.append(f"{chart.name}-{chart.version}")
                    trace = f"{chart.name}-{chart.version} already exists"
                    self._log_progress(Trace.TRACE, trace, idx, total_charts, progress)
                    continue

                # pull the source chart
                pull_command = ["helm", "pull", f"{chart.repo_url}/{chart.name}-{chart.version}.tgz"]
                return_code = self._run_command(
                    pull_command, f"Pulling {chart.name}-{chart.version}", idx, total_charts, progress
                )
                if return_code == 0:
                    upload_success.append(f"{chart.name}-{chart.version}")
                else:
                    upload_failures.append(f"{chart.name}-{chart.version}: Failed to download")

                # push the chart to ECR
                push_command = ["helm", "push", f"{chart.name}-{chart.version}.tgz", f"oci://{ecr_url}/{prefix}"]
                return_code = self._run_command(
                    push_command, f"Pushing {chart.name}-{chart.version}", idx, total_charts, progress
                )
                if return_code == 0:
                    self._clean_chart_temp_files(chart)
                    upload_success.append(f"{chart.name}-{chart.version}")
                else:
                    upload_failures.append(f"{chart.name}-{chart.version}: Failed to push")

        return UploadResult(failures=upload_failures, exists=upload_exists, success=upload_success)

    def helm_upload_zip(
        self, zip_file: str, prefix: str, regions: list[str] = None, progress: Optional[ProgressCallback] = None
    ) -> UploadResult:
        temp_dir = tempfile.mkdtemp()
        organization_id, root_ou_id, customers_ou_id = self._get_organizations()

        upload_failures = []
        upload_exists = []
        upload_success = []

        ecr_regions = regions if regions else [self.config.universe.region]

        for ecr_region in ecr_regions:
            self.logger.info(f"Uploading ({zip_file}) Helm charts to ECR in region {ecr_region}")
            sts_client = self._aws_shared_session.client("sts")
            ecr_client = self._aws_shared_session.client("ecr", region_name=ecr_region)
            if not self._helm_login(ecr_client):
                raise RuntimeError("Failed to login to ECR with Helm")

            account_id = sts_client.get_caller_identity()["Account"]
            ecr_url = f"{account_id}.dkr.ecr.{ecr_region}.amazonaws.com"

            try:
                # extract the zip file
                with zipfile.ZipFile(zip_file, "r") as zip_ref:
                    zip_ref.extractall(temp_dir)

                # find all tgz files in the extracted directory (recursively)
                tgz_files = []
                for root, _dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith(".tgz"):
                            tgz_files.append(os.path.join(root, file))

                if not tgz_files:
                    raise RuntimeError("No .tgz files found in the zip archive")

                total_charts = len(tgz_files)
                self._log_progress(Trace.INFO, f"Uploading {total_charts} charts from zip", 0, total_charts, progress)

                for idx, tgz_file in enumerate(tgz_files, start=1):
                    chart_name = None
                    chart_version = None

                    try:
                        # read chart contents
                        chart_name, chart_version, repo_name = self._extract_chart_from_tgz(
                            chart_name, chart_version, prefix, tgz_file
                        )

                        # apply the necessary permissions to the repository
                        self._apply_policy(ecr_client, repo_name, organization_id, root_ou_id, customers_ou_id)

                        # check if the chart already exists in ECR
                        exists, error = self._chart_exists_in_ecr(ecr_client, repo_name, chart_version)
                        if error:
                            upload_failures.append(f"{chart_name}-{chart_version}: {error}")
                            trace = f"Error for {chart_name}-{chart_version}: {error}"
                            self._log_progress(Trace.WARN, trace, idx, total_charts, progress)
                            continue

                        if exists:
                            upload_exists.append(f"{chart_name}-{chart_version}")
                            trace = f"{chart_name}-{chart_version} already exists"
                            self._log_progress(Trace.TRACE, trace, idx, total_charts, progress)
                            continue

                        # push the chart to ECR
                        push_command = ["helm", "push", tgz_file, f"oci://{ecr_url}/{prefix}"]
                        return_code = self._run_command(
                            push_command, f"Pushing {chart_name}-{chart_version}", idx, total_charts, progress
                        )

                        if return_code == 0:
                            upload_success.append(f"{chart_name}-{chart_version}")
                            self._log_progress(Trace.INFO, f"Uploaded {chart_name}-{chart_version}", idx, total_charts)
                        else:
                            upload_failures.append(f"{chart_name}-{chart_version}: Failed to push")
                            self._log_progress(
                                Trace.WARN, f"Failed to push {chart_name}-{chart_version}", idx, total_charts
                            )

                    except Exception as e:
                        upload_failures.append(f"{os.path.basename(tgz_file)}: {e}")
                        self._log_progress(
                            Trace.WARN, f"Error processing {os.path.basename(tgz_file)}: {e}", idx, total_charts
                        )

            except zipfile.BadZipFile as e:
                raise RuntimeError("The provided file is not a valid zip archive") from e
            except Exception as e:
                raise RuntimeError(f"Error extracting zip file: {e}") from e
            finally:
                try:
                    subprocess.run(["rm", "-rf", temp_dir], check=True)
                except Exception as e:
                    self.logger.error(f"Failed to clean up {temp_dir}: {e}")

        return UploadResult(failures=upload_failures, exists=upload_exists, success=upload_success)

    def docker_upload_images(
        self, images: list[str], prefix: str, regions: list[str] = None, progress: Optional[ProgressCallback] = None
    ) -> UploadResult:
        organization_id, root_ou_id, customers_ou_id = self._get_organizations()

        upload_failures = []
        upload_exists = []
        upload_success = []
        ecr_regions = regions if regions else [self.config.universe.region]

        for ecr_region in ecr_regions:
            self.logger.info(f"Uploading ({len(images)}) Docker images to ECR in region {ecr_region}")

            ecr_client = self._aws_shared_session.client("ecr", region_name=ecr_region)
            sts_client = self._aws_shared_session.client("sts")
            account_id = sts_client.get_caller_identity()["Account"]
            new_registry = f"{account_id}.dkr.ecr.{ecr_region}.amazonaws.com"

            if not self._docker_login(ecr_client):
                raise RuntimeError("Failed to login to ECR with Docker")

            total_images = len(images)
            self._log_progress(Trace.INFO, f"Uploading {total_images} images", 0, total_images, progress)

            for idx, image in enumerate(images, start=1):
                try:
                    self.logger.info(f"Processing image: {image}")

                    # validate and check if exists
                    ecr_image, repo_name = self._update_image_registry(image, prefix, new_registry)
                    if not ecr_image:
                        upload_failures.append(f"{image}: Invalid format")
                        self._log_progress(Trace.WARN, f"Invalid format for image {image}", idx, total_images, progress)
                        continue

                    image_tag = ecr_image.split(":")[-1]
                    self._apply_policy(ecr_client, repo_name, organization_id, root_ou_id, customers_ou_id)

                    if self._image_exists_in_ecr(ecr_client, repo_name, image_tag):
                        upload_exists.append(f"{image}-{image_tag}: Already exists")
                        self._log_progress(
                            Trace.TRACE, f"{image}-{image_tag} already exists", idx, total_images, progress
                        )
                        continue

                    # parse image source
                    if image.startswith("stratio-releases.repo.stratio.com"):
                        source_image, _ = self._update_image_registry(image, "", "qa.int.stratio.com")
                    else:
                        source_image, _ = self._update_image_registry(image, None, None)

                    if not source_image:
                        upload_failures.append(f"{image}: Unable to parse source image")
                        self._log_progress(
                            Trace.WARN, f"Unable to parse source image {image}", idx, total_images, progress
                        )
                        continue

                    # pull the source image
                    pull_command = ["sudo", "docker", "pull", source_image]
                    return_code = self._run_command(
                        pull_command, f"Pulling {source_image}", idx, total_images, progress
                    )
                    if return_code != 0:
                        upload_failures.append(f"{image}: Pull failed")
                        self._log_progress(Trace.WARN, f"Pull failed for image {image}", idx, total_images, progress)
                        continue

                    # tag the image for ECR
                    tag_command = ["sudo", "docker", "tag", source_image, ecr_image]
                    return_code = self._run_command(
                        tag_command, f"Tagging {source_image} as {ecr_image}", idx, total_images, progress
                    )
                    if return_code != 0:
                        upload_failures.append(f"{image}: Tagging failed")
                        self._log_progress(Trace.WARN, f"Tagging failed for image {image}", idx, total_images, progress)
                        continue

                    # push the image to ECR
                    push_command = ["sudo", "docker", "push", ecr_image]
                    return_code = self._run_command(push_command, f"Pushing {ecr_image}", idx, total_images, progress)
                    if return_code == 0:
                        # Remove local images to save space
                        rmi_command = ["sudo", "docker", "rmi", source_image]
                        self._run_command(rmi_command, f"Removing {source_image}", idx, total_images, progress)
                        rmi_command = ["sudo", "docker", "rmi", ecr_image]
                        self._run_command(rmi_command, f"Removing {ecr_image}", idx, total_images, progress)
                        upload_success.append(ecr_image)
                        self._log_progress(Trace.INFO, f"Uploaded {ecr_image}", idx, total_images, progress)
                    else:
                        upload_failures.append(f"{image}: Push failed")
                        self._log_progress(Trace.WARN, f"Push failed for image {image}", idx, total_images, progress)
                except Exception as e:
                    self.logger.error(f"Error processing image: {e}")
                    upload_failures.append(f"{image}: Unexpected error ({e})")
                    self._log_progress(
                        Trace.WARN, f"Unexpected error for image {image}: {e}", idx, total_images, progress
                    )

        return UploadResult(failures=upload_failures, exists=upload_exists, success=upload_success)

    def docker_upload_file(
        self, images_file: str, prefix: str, regions: list[str] = None, progress: Optional[ProgressCallback] = None
    ) -> UploadResult:
        with open(images_file) as file:
            images = [line.strip() for line in file.readlines() if line.strip()]
            return self.docker_upload_images(images, prefix, regions, progress)

    def delete_repository_prefix(
        self, prefix: str, regions: list[str] = None, progress: Optional[ProgressCallback] = None
    ) -> DeleteResult:
        delete_successes = []
        delete_failures = []

        ecr_regions = regions if regions else [self.config.universe.region]

        for region in ecr_regions:
            ecr_client = self._aws_shared_session.client("ecr", region_name=region)

            paginator = ecr_client.get_paginator("describe_repositories")
            repositories = []
            for page in paginator.paginate():
                for repo in page.get("repositories", []):
                    if repo["repositoryName"].startswith(prefix):
                        repositories.append(repo["repositoryName"])

            if not repositories:
                self.logger.warn(f"No repositories found with prefix '{prefix}' in region {region}.")
                continue

            self.logger.info(f"Deleting repositories with prefix {prefix} in region {region}")
            total_repositories = len(repositories)
            for idx, repo_name in enumerate(repositories, start=1):
                try:
                    ecr_client.delete_repository(repositoryName=repo_name, force=True)
                    delete_successes.append(f"{repo_name} (Region: {region})")
                    self._log_progress(Trace.INFO, f"Deleted {repo_name}", idx, total_repositories, progress)
                except ecr_client.exceptions.RepositoryNotFoundException:
                    delete_failures.append(f"{repo_name} (Region: {region}): Not found")
                    self._log_progress(
                        Trace.WARN, f"Repository {repo_name} not found", idx, total_repositories, progress
                    )
                except Exception as e:
                    delete_failures.append(f"{repo_name} (Region: {region}): {e}")
                    self._log_progress(
                        Trace.WARN, f"Failed to delete {repo_name}: {e}", idx, total_repositories, progress
                    )

        return DeleteResult(success=delete_successes, failures=delete_failures)

    def delete_repository(
        self,
        repository: str,
        tag: Optional[str] = None,
        regions: list[str] = None,
        progress: Optional[ProgressCallback] = None,
    ) -> DeleteResult:
        delete_successes = []
        delete_failures = []

        ecr_regions = regions if regions else [self.config.universe.region]
        total_regions = len(ecr_regions)
        for idx, region in enumerate(ecr_regions, start=1):
            ecr_client = self._aws_shared_session.client("ecr", region_name=region)

            try:
                if tag:
                    image_ids = [{"imageTag": tag}]
                    response = ecr_client.batch_delete_image(repositoryName=repository, imageIds=image_ids)
                    deleted = response.get("imageIds", [])
                    failures = response.get("failures", [])

                    for img in deleted:
                        delete_successes.append(f"{repository}:{img.get('imageTag')} (Region: {region})")
                        self._log_progress(
                            Trace.INFO, f"Deleted {repository}:{img.get('imageTag')}", idx, total_regions, progress
                        )
                    for failure in failures:
                        trace = (
                            f"{repository}:{failure.get('imageId', {}).get('imageTag')} (Region: {region}): "
                            f"{failure.get('failureReason')}"
                        )
                        delete_failures.append(trace)
                        self._log_progress(Trace.WARN, f"Failed to delete {trace}", idx, total_regions, progress)
                else:
                    ecr_client.delete_repository(repositoryName=repository, force=True)
                    delete_successes.append(f"{repository} (Region: {region})")
                    self._log_progress(Trace.INFO, f"Deleted {repository}", idx, total_regions, progress)
            except ecr_client.exceptions.RepositoryNotFoundException:
                delete_failures.append(f"{repository} (Region: {region}): Not found")
                self._log_progress(Trace.WARN, f"Repository {repository} not found", idx, total_regions, progress)

        return DeleteResult(success=delete_successes, failures=delete_failures)

    def _run_command(
        self,
        command: list[str],
        description: str,
        current: int,
        total: int,
        progress_callback: Optional[ProgressCallback] = None,
    ):
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True
        )

        def handle_stream(stream, progress):
            for line in stream:
                self.logger.info(f"{description}: {line.strip()}")
                if progress:
                    progress.trace(line.strip(), current, total)

        # Start threads to handle stdout and stderr
        stdout_thread = threading.Thread(target=handle_stream, args=(process.stdout, progress_callback))
        stderr_thread = threading.Thread(target=handle_stream, args=(process.stderr, progress_callback))
        stdout_thread.start()
        stderr_thread.start()

        # Wait for the process to complete
        process.wait()
        stdout_thread.join()
        stderr_thread.join()

        return process.returncode

    def _helm_login(self, ecr_client: BaseClient) -> bool:
        auth_data = ecr_client.get_authorization_token()
        token = base64.b64decode(auth_data["authorizationData"][0]["authorizationToken"]).decode()
        username, password = token.split(":")
        ecr_url = auth_data["authorizationData"][0]["proxyEndpoint"]
        result = subprocess.run(
            ["helm", "registry", "login", "-u", username, "-p", password, ecr_url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode != 0:
            self.logger.error("Error logging into ECR with Helm")
            return False
        else:
            return True

    def _docker_login(self, ecr_client) -> bool:
        try:
            auth_data = ecr_client.get_authorization_token()
            token = base64.b64decode(auth_data["authorizationData"][0]["authorizationToken"]).decode()
            username, password = token.split(":")
            ecr_url = auth_data["authorizationData"][0]["proxyEndpoint"]
            login_command = ["sudo", "docker", "login", "-u", username, "-p", password, ecr_url]
            result_code = self._run_command(login_command, "Docker login", 0, 0, None)
            if result_code != 0:
                self.logger.error(f"Docker login failed for {ecr_url}")
                return False
            else:
                self.logger.info(f"Docker logged in to {ecr_url}")
                return True
        except Exception as e:
            self.logger.error(f"Docker login error: {e}")
            return False

    def _apply_policy(
        self, ecr_client: BaseClient, repository_name: str, organization_id: str, root_ou_id: str, customers_ou_id: str
    ) -> bool:
        policy_text = f"""{{
            "Version": "2012-10-17",
            "Statement": [
            {{
                "Sid": "AllowPull",
                "Effect": "Allow",
                "Principal": "*",
                "Action": [
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:BatchGetImage",
                    "ecr:DescribeImages",
                    "ecr:DescribeRepositories",
                    "ecr:GetDownloadUrlForLayer",
                    "ecr:ListImages"
                ],
                "Condition": {{
                  "ForAnyValue:StringLike": {{
                    "aws:PrincipalOrgPaths": "{organization_id}/{root_ou_id}/{customers_ou_id}*"
                }}
                }}
            }}
            ]
        }}"""

        try:
            ecr_client.describe_repositories(repositoryNames=[repository_name])
        except ecr_client.exceptions.RepositoryNotFoundException:
            ecr_client.create_repository(repositoryName=repository_name)
        except Exception as e:
            self.logger.error(f"Error checking repository '{repository_name}': {e}")
            return False

        try:
            ecr_client.set_repository_policy(repositoryName=repository_name, policyText=policy_text)
        except ecr_client.exceptions.InvalidParameterException as e:
            self.logger.error(f"Failed to set policy for repository '{repository_name}': {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error setting policy for repository '{repository_name}': {e}")
            return False

        return True

    def _chart_exists_in_ecr(
        self, ecr_client: BaseClient, repository_name: str, chart_tag: str
    ) -> tuple[bool, Optional[str]]:
        try:
            response = ecr_client.describe_images(repositoryName=repository_name, imageIds=[{"imageTag": chart_tag}])
            return bool(response.get("imageDetails")), None
        except ecr_client.exceptions.ImageNotFoundException:
            return False, None
        except Exception as e:
            self.logger.error(f"Error checking if chart exists in ECR: {e}")
            return False, f"{e}"

    def _extract_chart_from_tgz(self, chart_name, chart_version, prefix, tgz_file):
        with tarfile.open(tgz_file, "r:gz") as tar:
            # find the Chart.yaml file
            chart_yaml_member = None
            for member in tar.getmembers():
                if os.path.basename(member.name) == "Chart.yaml":
                    chart_yaml_member = member
                    break

            if not chart_yaml_member:
                raise FileNotFoundError(f"Chart.yaml not found in {tgz_file}")

            # extract Chart.yaml content
            chart_yaml_file = tar.extractfile(chart_yaml_member)
            if chart_yaml_file is None:
                raise FileNotFoundError(f"Unable to extract Chart.yaml from {tgz_file}")

            chart_yaml = yaml.safe_load(chart_yaml_file)
            chart_name = chart_yaml.get("name")
            chart_version = chart_yaml.get("version")
            repo_name = f"{prefix}/{chart_name}"

            if not chart_name or not chart_version:
                raise ValueError(f"Chart.yaml in {tgz_file} is missing 'name' or 'version' fields.")
        return chart_name, chart_version, repo_name

    def _update_image_registry(
        self, image: str, prefix: Optional[str], new_registry: Optional[str]
    ) -> tuple[Optional[str], Optional[str]]:
        try:
            parts = image.split(":")

            # Check if there's a port (by having 2 or more parts before the version)
            if len(parts) > 2:
                # Port is present in the registry
                registry_repo = ":".join(parts[:2])
                version = parts[2] if len(parts) > 2 else "latest"
            else:
                # No port in the registry
                registry_repo = parts[0]
                version = parts[1] if len(parts) > 1 else "latest"

            registry = registry_repo.split("/")[0]
            repo_name = "/".join(registry_repo.split("/")[1:])

            if prefix:
                repo_name = f"{prefix}/{repo_name}"

            new_image = f"{new_registry}/{repo_name}:{version}" if new_registry else f"{registry}/{repo_name}:{version}"

            return new_image, repo_name
        except Exception as e:
            self.logger.error(f"Error parsing image '{image}': {e}")
            return None, None

    def _image_exists_in_ecr(self, ecr_client, repository_name, image_tag):
        try:
            ecr_client.describe_images(repositoryName=repository_name, imageIds=[{"imageTag": image_tag}])
            return True
        except ecr_client.exceptions.RepositoryNotFoundException:
            return False
        except ecr_client.exceptions.ImageNotFoundException:
            return False
        except Exception as e:
            self.logger.error(f"Error checking image existence: {e}")
            return False

    def _get_organizations(self):
        org_client = self._aws_root_session.client("organizations")

        # extract organization_id and root ouid
        roots = org_client.list_roots()
        root_oid = roots["Roots"][0]["Id"]
        organization_id = org_client.describe_organization()["Organization"]["Id"]

        # extract customers ouid
        paginator = org_client.get_paginator("list_organizational_units_for_parent")
        customers_ou_id = next(
            (
                ou["Id"]
                for page in paginator.paginate(ParentId=root_oid)
                for ou in page["OrganizationalUnits"]
                if ou["Name"] == self.config.universe.customers_ou_name
            ),
            None,
        )

        return organization_id, root_oid, customers_ou_id

    def _clean_chart_temp_files(self, chart):
        try:
            os.remove(f"{chart.name}-{chart.version}.tgz")
        except Exception as e:
            self.logger.warn(f"Unable to remove temporary file {chart.name}-{chart.version}.tgz: {e}")

    @staticmethod
    def chart_overrides_to_list(charts_file: str) -> list[Chart]:
        with open(charts_file) as file:
            yaml_content = yaml.safe_load(file)
            chart_list = yaml_content.get("helm_charts_override", [])
            formatted_charts = [
                Chart(repo_url=chart["repo_url"], name=chart["name"], version=chart["version"]) for chart in chart_list
            ]
        return formatted_charts

    @staticmethod
    def _log_progress(level: str, message: str, current: int, total: int, progress: Optional[ProgressCallback] = None):
        if progress:
            if level.lower() == "info":
                progress.info(message, current, total)
            elif level.lower() == "warn":
                progress.warn(message, current, total)
            elif level.lower() == "trace":
                progress.trace(message, current, total)

    @staticmethod
    def _initialize_aws_session(session: Optional[ApiSession]) -> Optional[boto3.Session]:
        if not session:
            return None
        if isinstance(session, ProfileApiSession):
            return boto3.Session(profile_name=session.profile_name)
        elif isinstance(session, CredentialsApiSession):
            return boto3.Session(
                aws_access_key_id=session.key_id,
                aws_secret_access_key=session.secret_key,
                region_name=session.region_name,
            )
        return None

    class Builder(BaseRepositoriesClient.Builder):
        def build(self):
            # Determine which session to use:
            # 1. Use the session provided via with_session
            # 2. Otherwise, use the session from config.clusters.session
            shared_session = self.shared_session
            root_session = self.root_session
            if not shared_session and self.config and self.config.sessions.shared:
                shared_session = self.config.sessions.shared.to_api_session()

            if not root_session and self.config and self.config.sessions.root:
                root_session = self.config.sessions.root.to_api_session()

            aws_shared_session = RepositoriesClient._initialize_aws_session(shared_session)
            aws_root_session = RepositoriesClient._initialize_aws_session(root_session)
            return RepositoriesClient(
                logger=self.logger,
                root_session=root_session,
                shared_session=shared_session,
                aws_root_session=aws_root_session,
                aws_shared_session=aws_shared_session,
                config=self.config,
            )
