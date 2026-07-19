import tomllib
from pathlib import Path
from typing import Literal
from pydantic import BaseModel


class ContextConfig(BaseModel):
    enabled: bool = True
    trace_id: bool = True
    endpoint: bool = True


class LoggerConfig(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG"
    format: Literal["json", "logfmt", "psv"] = "psv"
    indent: bool = False
    indent_size: int = 2
    # rotation: Literal["daily", "size", "none"] = "daily"
    context: ContextConfig = ContextConfig()


LOG_CONFIG = LoggerConfig.model_validate(tomllib.loads(Path("logger.toml").read_text()))
