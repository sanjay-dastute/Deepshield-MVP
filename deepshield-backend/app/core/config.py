from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

    PROJECT_NAME: str = "DeepShield"
    API_V1_STR: str = "/api/v1"
    
    # MongoDB settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "deepshield"
    mongodb_db: str = "deepshield"  # For compatibility
    
    # JWT settings
    SECRET_KEY: str = "your-secret-key"
    jwt_secret: str = "your-secret-key-here"  # For compatibility
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Instagram API settings
    INSTAGRAM_APP_ID: str = "1112199003401971"
    INSTAGRAM_APP_SECRET: str = "33191e18dd0aa8db81049ee756d2f324"
    INSTAGRAM_ACCESS_TOKEN: str = "IGAAPzigKEbvNBZAE1pMG9uUTZAxR0NzSTRIdEE5SXNhc0hRMHVZAWWhsNjcxSzVUa2w1ZAHFyYmNoLVU3bXJvZA0N5YUdhWC1nN2V0WWtoSHJMS3ZAPTFB6am82SFZAwSG1uUXNJcU1hUDkxSFdVa2t4Tl9zbDNQcElTNGtkTmRVWkZADZAwZDZD"
    
    # Google Cloud Translation API settings
    GOOGLE_CLOUD_API_KEY: Optional[str] = None
    
    # Email settings
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    FROM_EMAIL: str = "noreply@deepshield.ai"
    
    # SMS settings
    SMS_API_KEY: Optional[str] = None
    SMS_API_URL: str = "https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
    SMS_FROM_NUMBER: Optional[str] = None

settings = Settings()
