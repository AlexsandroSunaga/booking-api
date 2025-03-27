from src.config.settings.base import BackendBaseSettings
from src.config.settings.environments import Environment


class BackendStageSettings(BackendBaseSettings):
    environment: Environment = Environment.STAGING
