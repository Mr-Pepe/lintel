"""Configuration file parsing and utilities."""

import sys
from configparser import ConfigParser
from configparser import Error as ConfigParserError
from pathlib import Path
from typing import Optional, Set

from pydantic import BaseModel, Extra, ValidationError, validator

from pydocstyle import Convention

from ._version import __version__

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


SETUP_CFG = "setup.cfg"
TOX_INI = "tox.ini"
PYPROJECT_TOML = "pyproject.toml"

PROJECT_CONFIG_FILES = (SETUP_CFG, TOX_INI, PYPROJECT_TOML)


class Configuration(BaseModel):
    """The docstring checker configuration."""

    convention: Convention = Convention.PEP257
    select: Set[str] = set()
    ignore: Set[str] = set()
    match: str = r'(?!test_).*\.py'
    match_dir: str = r'[^\.].*'
    ignore_decorators: Optional[str] = None
    property_decorators: Set[str] = {
        "property",
        "cached_property",
        "functools.cached_property",
    }
    ignore_inline_noqa: bool = False
    verbose: bool = False

    @validator('select', pre=True)
    def parse_select(cls, v: str) -> Set[str]:
        return set(v.split(","))

    @validator('ignore', pre=True)
    def parse_ignore(cls, v: str) -> Set[str]:
        return set(v.split(","))

    @validator('property_decorators', pre=True)
    def parse_property_decorators(cls, v: str) -> Set[str]:
        return set(v.split(","))

    class Config:
        extra = Extra.forbid


def load_config(config_path: Path) -> Configuration:
    if config_path.is_file():
        return _load_config_file(config_path)

    for config_file in PROJECT_CONFIG_FILES:
        try:
            return _load_config_file(config_path / config_file)
        except (FileNotFoundError, IllegalConfiguration):
            pass

    return Configuration()


def _load_config_file(config_path: Path) -> Configuration:
    try:
        toml = tomllib.loads(config_path.read_text())["tool"]["pydocstyle"]
    except (tomllib.TOMLDecodeError, KeyError):
        toml = None

    try:
        parser = ConfigParser()
        parser.read(config_path)

        ini = parser["pydocstyle"]
    except (ConfigParserError, KeyError):
        ini = None

    config_dict = toml or ini

    try:
        return Configuration.parse_obj(config_dict)
    except ValidationError:
        raise IllegalConfiguration()


class IllegalConfiguration(Exception):
    """An exception for illegal configurations."""

    pass
