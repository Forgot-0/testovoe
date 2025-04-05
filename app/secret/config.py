from app.core.configs.base import BaseConfig


class SecretConfig(BaseConfig):
    SECRET_KEY: str


secret_config = SecretConfig()