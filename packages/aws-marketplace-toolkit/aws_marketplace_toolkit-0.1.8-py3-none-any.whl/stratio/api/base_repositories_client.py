# src/stratio/api/base_repositories_client.py
import logging
from abc import ABC, abstractmethod
from typing import Callable, Optional

from stratio.api.callbacks import ProgressCallback
from stratio.api.models import Chart, UploadResult
from stratio.api.models.repositories import DeleteResult
from stratio.api.session import ApiSession
from stratio.config import Config

logging.basicConfig(level=logging.INFO)


class BaseRepositoriesClient(ABC):
    """
    Abstract client definition for common operations on a Stratio AWS infrastructure.
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        root_session: Optional[ApiSession] = None,
        shared_session: Optional[ApiSession] = None,
        config: Optional[Config] = None,
    ):
        self.logger = logger or self._default_logger()
        self.root_session = root_session
        self.shared_session = shared_session
        self.config = config

    @abstractmethod
    def helm_upload_charts(
        self,
        charts: list[Chart],
        prefix: str,
        regions: list[str] = None,
        progress: Optional[Callable[[str, int, int], None]] = None,
    ) -> UploadResult:
        pass

    @abstractmethod
    def helm_upload_zip(
        self, zip_file: str, prefix: str, regions: list[str] = None, progress: Optional[ProgressCallback] = None
    ) -> UploadResult:
        pass

    @abstractmethod
    def docker_upload_images(
        self, images: list[str], prefix: str, regions: list[str] = None, progress: Optional[ProgressCallback] = None
    ) -> UploadResult:
        pass

    @abstractmethod
    def docker_upload_file(
        self, images_file: str, prefix: str, regions: list[str] = None, progress: Optional[ProgressCallback] = None
    ) -> UploadResult:
        pass

    @abstractmethod
    def delete_repository_prefix(
        self,
        prefix: str,
        regions: list[str] = None,
        progress: Optional[ProgressCallback] = None,
    ) -> DeleteResult:
        pass

    @abstractmethod
    def delete_repository(
        self,
        repository: str,
        tag: Optional[str] = None,
        regions: list[str] = None,
        progress: Optional[ProgressCallback] = None,
    ) -> DeleteResult:
        pass

    @staticmethod
    def _default_logger():
        logger = logging.getLogger("BaseClient")
        if not logger.handlers:
            # Prevent adding multiple handlers in interactive environments
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    class Builder:
        """
        Abstract Builder class for BaseClient.
        """

        def __init__(self):
            # public attributes
            self.logger: Optional[logging.Logger] = None
            self.shared_session: Optional[ApiSession] = None
            self.root_session: Optional[ApiSession] = None
            self.config: Optional[Config] = None

            # private attributes
            self._aws_shared_session = None

        def with_config(self, config: Config):
            self.config = config
            return self

        def with_logger(self, logger: logging.Logger):
            self.logger = logger
            return self

        def with_shared_session(self, session: ApiSession):
            self.shared_session = session
            return self

        def with_root_session(self, session: ApiSession):
            self.root_session = session
            return self

        @abstractmethod
        def build(self):
            pass
