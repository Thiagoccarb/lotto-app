import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")

class Settings(BaseSettings):
    class Config:
        env_file = f".env"

    # Application
    NAME: str = "lotto API"
    APPLICATION_NAME: str = "lotto-api"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "lotto API in Python"

    # Url
    

    # Database
    MONGO_URL: str = MONGO_URL
    MONGO_DB: str = MONGO_DB

settings = Settings()
