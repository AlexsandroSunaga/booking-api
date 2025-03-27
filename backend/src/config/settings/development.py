from src.config.settings.base import BackendBaseSettings
from src.config.settings.environments import Environment


class BackendDevSettings(BackendBaseSettings):
    environment: Environment = Environment.DEVELOPMENT
