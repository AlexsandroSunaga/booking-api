from src.config.settings.base import BackendBaseSettings
from src.config.settings.environments import Environment


class BackendProdSettings(BackendBaseSettings):
    environment: Environment = Environment.PRODUCTION
