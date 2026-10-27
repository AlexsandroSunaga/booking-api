import pytest
from pydantic import ValidationError

from src.config.settings.base import BackendBaseSettings


def test_placeholder_jwt_secret_is_allowed_in_development():
    settings = BackendBaseSettings(environment="development", jwt_secret="change-me")
    assert settings.jwt_secret == "change-me"


@pytest.mark.parametrize("environment", ["staging", "production"])
def test_placeholder_jwt_secret_is_rejected_outside_development(environment):
    with pytest.raises(ValidationError):
        BackendBaseSettings(environment=environment, jwt_secret="change-me")


def test_real_jwt_secret_is_accepted_in_production():
    settings = BackendBaseSettings(environment="production", jwt_secret="a-long-random-value")
    assert settings.environment.value == "production"
