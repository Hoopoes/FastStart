import tomllib
from os import getenv
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()

with open("pyproject.toml", "rb") as f:
    poetry: dict[str] = tomllib.load(f).get("tool", {}).get("poetry", {})
    name = poetry.get("name")
    description = poetry.get("description")
    version = poetry.get("version")

class ConfigClass(BaseModel):
    app_name: str
    description: str
    version: str
    root_path: str
    api_key: Optional[str]

CONFIG = ConfigClass(
    app_name = name,
    description = description,
    version = version,
    root_path="/api/v1",
    api_key = getenv("API_KEY") if getenv("API_KEY") else None
)
