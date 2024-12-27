from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # MongoDB settings
    mongodb_url: str
    mongodb_db: str
    
    # JWT settings
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    
    # Instagram API settings
    instagram_app_id: str = "1112199003401971"
    instagram_app_secret: str = "33191e18dd0aa8db81049ee756d2f324"
    instagram_access_token: str = "IGAAPzigKEbvNBZAE1pMG9uUTZAxR0NzSTRIdEE5SXNhc0hRMHVZAWWhsNjcxSzVUa2w1ZAHFyYmNoLVU3bXJvZA0N5YUdhWC1nN2V0WWtoSHJMS3ZAPTFB6am82SFZAwSG1uUXNJcU1hUDkxSFdVa2t4Tl9zbDNQcElTNGtkTmRVWkZADZAwZDZD"
    instagram_account_id: str = "17841451799717870"
    
    # Google Cloud Vision API settings
    google_cloud_project: str = "deepshield-mvp"
    google_application_credentials: str = ""  # Will be set via environment variable
    
    # Translation API settings
    translation_api_key: str = ""  # Will be set via environment variable
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
