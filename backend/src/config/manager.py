from functools import lru_cache

from src.config.settings.base import BackendBaseSettings
from src.config.settings.development import BackendDevSettings
from src.config.settings.environments import Environment


class BackendSettingsFactory:
    @staticmethod
    def build(environment: str | None = None) -> BackendBaseSettings:
        env = (environment or "development").lower()
        if env == Environment.PRODUCTION.value:
            from src.config.settings.production import BackendProdSettings

            return BackendProdSettings()
        if env == Environment.STAGING.value:
            from src.config.settings.staging import BackendStageSettings

            return BackendStageSettings()
        return BackendDevSettings()


@lru_cache
def get_settings() -> BackendBaseSettings:
    return BackendSettingsFactory.build()
