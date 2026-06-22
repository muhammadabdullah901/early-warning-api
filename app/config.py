"""
Central configuration for the whole app.

Instead of writing the ERP url / api key in many files, we keep them in ONE
place here. Values are read from the .env file (or system environment).
Any other file can do:  from app.config import settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # General
    app_name: str = "Early Warning System API"

    # ERP integration settings
    erp_base_url: str = "https://erp.example.com/api"
    erp_api_key: str = "changeme"
    erp_mock_mode: bool = True  # True = use fake data, no real network calls

    # Tell pydantic to load values from a file named ".env"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# A single shared settings object used across the app.
settings = Settings()
