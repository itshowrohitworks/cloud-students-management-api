# Loads env variables: Secret Entries are kept here!
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings() # type:ignore