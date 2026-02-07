import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field, ValidationError
from src.models import SourceConfig, FetchSettings
from src.utils.logger import get_logger

logger = get_logger()


class AppConfig(BaseModel):
    """Application configuration schema"""
    name: str = "AutoNews"
    timezone: str = "UTC"


class SchedulerConfig(BaseModel):
    """Scheduler configuration schema"""
    enabled: bool = True
    cron: str = "0 8 * * *"


class StorageConfig(BaseModel):
    """Storage configuration schema"""
    type: str = "json"
    output_dir: str = "data/processed"
    exports_dir: str = "data/exports"
    organize_by_date: bool = True
    formats: List[str] = ["json"]


class DeduplicationConfig(BaseModel):
    """Deduplication configuration schema"""
    enabled: bool = True
    history_file: str = "data/history/hashes.json"
    method: str = "content_hash"


class SummarizationConfig(BaseModel):
    """Summarization configuration schema"""
    enabled: bool = True
    max_length: int = 200
    method: str = "extractive"


class ClassificationConfig(BaseModel):
    """Classification configuration schema"""
    enabled: bool = True
    method: str = "keyword"


class ProcessingConfig(BaseModel):
    """Processing configuration schema"""
    deduplication: DeduplicationConfig
    summarization: SummarizationConfig
    classification: ClassificationConfig


class NotificationChannel(BaseModel):
    """Notification channel configuration"""
    type: str


class NotificationsConfig(BaseModel):
    """Notifications configuration schema"""
    enabled: bool = True
    channels: List[NotificationChannel]


class LoggingConfig(BaseModel):
    """Logging configuration schema"""
    level: str = "INFO"
    file: str = "logs/autonews.log"
    max_bytes: int = 10485760
    backup_count: int = 5


class ErrorHandlingConfig(BaseModel):
    """Error handling configuration schema"""
    max_retries: int = 3
    retry_delay: int = 5
    continue_on_error: bool = True


class Config(BaseModel):
    """Main configuration schema"""
    app: AppConfig
    scheduler: SchedulerConfig
    storage: StorageConfig
    processing: ProcessingConfig
    notifications: NotificationsConfig
    logging: LoggingConfig
    error_handling: ErrorHandlingConfig


class ConfigManager:
    """Manages application configuration"""

    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "config.yaml"
        self.sources_file = self.config_dir / "sources.yaml"
        self._config: Optional[Config] = None
        self._sources: Optional[List[SourceConfig]] = None
        self._fetch_settings: Optional[FetchSettings] = None

        # Load and validate configuration
        self.load_config()
        self.load_sources()

    def load_config(self) -> Config:
        """Load and validate main configuration"""
        try:
            with open(self.config_file, 'r') as f:
                config_data = yaml.safe_load(f)

            self._config = Config(**config_data)
            logger.info(f"Configuration loaded from {self.config_file}")
            return self._config

        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_file}")
            raise
        except ValidationError as e:
            logger.error(f"Configuration validation failed: {e}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {e}")
            raise

    def load_sources(self) -> List[SourceConfig]:
        """Load and validate sources configuration"""
        try:
            with open(self.sources_file, 'r') as f:
                sources_data = yaml.safe_load(f)

            self._sources = [
                SourceConfig(**source)
                for source in sources_data.get('sources', [])
            ]

            # Load fetch settings
            fetch_data = sources_data.get('fetch_settings', {})
            self._fetch_settings = FetchSettings(**fetch_data)

            logger.info(f"Loaded {len(self._sources)} news sources")
            return self._sources

        except FileNotFoundError:
            logger.error(f"Sources file not found: {self.sources_file}")
            raise
        except Exception as e:
            logger.error(f"Error loading sources: {e}")
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation

        Example: config.get('storage.output_dir')
        """
        if not self._config:
            self.load_config()

        keys = key.split('.')
        value = self._config.model_dump()

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def get_sources(self) -> List[SourceConfig]:
        """Get list of configured sources"""
        if not self._sources:
            self.load_sources()
        return self._sources

    def get_fetch_settings(self) -> FetchSettings:
        """Get fetch settings"""
        if not self._fetch_settings:
            self.load_sources()
        return self._fetch_settings

    def validate(self) -> bool:
        """Validate configuration"""
        try:
            if not self._config:
                self.load_config()
            if not self._sources:
                self.load_sources()

            # Check if required directories exist or can be created
            required_dirs = [
                self.get('storage.output_dir'),
                self.get('storage.exports_dir'),
                Path(self.get('processing.deduplication.history_file')).parent,
                Path(self.get('logging.file')).parent,
            ]

            for dir_path in required_dirs:
                Path(dir_path).mkdir(parents=True, exist_ok=True)

            logger.info("Configuration validation successful")
            return True

        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False
