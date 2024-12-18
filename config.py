from os import getenv
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()


class ConfigClass(BaseModel):
    app_name: str
    description: str
    root_path: str
    api_key: Optional[str]

CONFIG = ConfigClass(
    app_name = "<APP_NAME>",
    description = "<APP_DESCRIPTION>",
    root_path="/api/v1",
    api_key = getenv("API_KEY") if getenv("API_KEY") else None
)