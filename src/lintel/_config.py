"""Configuration file parsing and utilities."""

import logging
import re
import sys
from configparser import ConfigParser
from configparser import Error as ConfigParserError
from pathlib import Path
from typing import Optional, Set, Union

from pydantic import BaseModel, Extra, ValidationError, validator

from lintel import Convention

from ._version import __version__

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


_logger = logging.getLogger(__name__)

SETUP_CFG = "setup.cfg"
TOX_INI = "tox.ini"
PYPROJECT_TOML = "pyproject.toml"

PROJECT_CONFIG_FILES = (SETUP_CFG, TOX_INI, PYPROJECT_TOML)

DEFAULT_MATCH = r'(?!test_).*\.py$'
DEFAULT_MATCH_DIR = r'[^\.].*'
DEFAULT_PROPERTY_DECORATORS = {
    "property",
    "cached_property",
    "functools.cached_property",
}


class Configuration(BaseModel):
    """The docstring checker configuration."""

    convention: Convention = Convention.DEFAULT
    select: Set[str] = set()
    ignore: Set[str] = set()
    add_select: Set[str] = set()
    add_ignore: Set[str] = set()
    match: str = DEFAULT_MATCH
    match_dir: str = DEFAULT_MATCH_DIR
    ignore_decorators: Optional[str] = None
    property_decorators: Set[str] = DEFAULT_PROPERTY_DECORATORS
    ignore_inline_noqa: bool = False
    verbose: bool = False

    @validator('select', pre=True)
    def parse_select(cls, v: Union[str, Set[str]]) -> Set[str]:
        if isinstance(v, str):
            return set(re.findall(r"D\d+\b", v))
        return v

    @validator('ignore', pre=True)
    def parse_ignore(cls, v: Union[str, Set[str]]) -> Set[str]:
        if isinstance(v, str):
            return set(re.findall(r"D\d+\b", v))
        return v

    @validator('add_select', pre=True)
    def parse_add_select(cls, v: Union[str, Set[str]]) -> Set[str]:
        if isinstance(v, str):
            return set(re.findall(r"D\d+\b", v))
        return v

    @validator('add_ignore', pre=True)
    def parse_add_ignore(cls, v: Union[str, Set[str]]) -> Set[str]:
        if isinstance(v, str):
            return set(re.findall(r"D\d+\b", v))
        return v

    @validator('property_decorators', pre=True)
    def parse_property_decorators(cls, v: Union[str, Set[str]]) -> Set[str]:
        if isinstance(v, str):
            return set(v.split(",")) - {""}
        return v

    class Config:
        extra = Extra.forbid


def load_config(config_path: Path) -> Configuration:
    if not config_path.exists():
        _logger.error(
            "Failed to load configuration from '%s' because that path does not exist.", config_path
        )
        raise IllegalConfiguration()

    if config_path.is_file():
        try:
            return _load_config_file(config_path)
        except ValueError:
            _logger.error("Configuration file %s does not contain a lintel section.", config_path)
            raise

    for config_file in PROJECT_CONFIG_FILES:
        try:
            return _load_config_file(config_path / config_file)
        except (FileNotFoundError, ValueError):
            pass

    return Configuration()


def _load_config_file(config_path: Path) -> Configuration:
    try:
        toml = tomllib.loads(config_path.read_text())["tool"]["lintel"]
    except (tomllib.TOMLDecodeError, KeyError):
        toml = None

    try:
        parser = ConfigParser()
        parser.read(config_path)

        ini = parser["lintel"]
    except (ConfigParserError, KeyError):
        ini = None

    config_dict = toml or ini

    if config_dict is None:
        raise ValueError(f"No lintel section found in '{config_path}'.")

    # Replace dashes with underscores in keys
    config_dict = {k.replace("-", "_"): v for k, v in config_dict.items()}

    try:
        return Configuration.parse_obj(config_dict)
    except ValidationError:
        raise IllegalConfiguration(f"Invalid lintel settings in '{config_path}'.")


class IllegalConfiguration(Exception):
    """An exception for illegal configurations."""

    pass
