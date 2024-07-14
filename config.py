from os import getenv
from dotenv import load_dotenv


load_dotenv()


class Config:
    app_name = "<APP_NAME>"
    description = "<APP_DESCRIPTION>"
    api_key = getenv("API_KEY")