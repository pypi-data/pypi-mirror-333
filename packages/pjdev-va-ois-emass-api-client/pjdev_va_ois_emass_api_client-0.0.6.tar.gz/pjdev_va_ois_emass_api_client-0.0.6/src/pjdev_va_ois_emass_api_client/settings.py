from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Context:
    settings: Optional["EmassSettings"] = None


__ctx = Context()


class EmassSettings(BaseSettings):
    api_url: str
    api_key: str
    client_cert_path: Path
    client_cert_key_path: Path
    client_cert_key_pass: str

    model_config = SettingsConfigDict(
        env_prefix="EMASS_", case_sensitive=False, extra="ignore"
    )


def init_settings(root: Path) -> None:
    __ctx.settings = EmassSettings(_env_file=root / ".env")


def get_settings() -> EmassSettings:
    if __ctx.settings is None:
        raise Exception("Must call init_settings first")
    return __ctx.settings
