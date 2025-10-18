from __future__ import annotations
import os
from dataclasses import dataclass

BASEDIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASEDIR, os.pardir))
DEFAULT_SQLITE = f"sqlite:///{os.path.join(PROJECT_ROOT, 'instance', 'dev.db')}"


@dataclass
class BaseConfig:
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_URL", DEFAULT_SQLITE)
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SESSION_PROTECTION: str = "strong"
    JSON_SORT_KEYS: bool = False
    

@dataclass
class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True


@dataclass
class TestingConfig(BaseConfig):
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"


@dataclass
class ProductionConfig(BaseConfig):
    DEBUG: bool = False


CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(name: str | None):
    if not name:
        name = os.environ.get("FLASK_ENV", "development").lower()
    config_cls = CONFIG_MAP.get(name, DevelopmentConfig)
    return config_cls()
