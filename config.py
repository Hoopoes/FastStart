import tomllib
from os import getenv
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()

with open("pyproject.toml", "rb") as f:
    poetry: dict[str] = tomllib.load(f).get("project", {})
    name = poetry.get("name")
    description = poetry.get("description")
    version = poetry.get("version")

class ConfigClass(BaseModel):
    app_name: str
    description: str
    version: str
    route_prefix: str
    root_path: Optional[str]
    api_key: Optional[str]

CONFIG = ConfigClass(
    app_name = name,
    description = description,
    version = version,
    route_prefix ="/api/v1",
    root_path = getenv("ROOT_PATH"),
    api_key = getenv("API_KEY") if getenv("API_KEY") else None
)
