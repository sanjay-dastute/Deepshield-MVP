from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "DeepShield"
    API_V1_STR: str = "/api/v1"
    
    # MongoDB settings
    MONGODB_URL: str = Field(default="mongodb://localhost:27017")
    MONGODB_DB: str = Field(default="deepshield")
    
    # JWT settings
    JWT_SECRET: str = Field(default="your-secret-key")
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_EXPIRE_MINUTES: int = Field(default=30)
    
    # Instagram API settings
    INSTAGRAM_APP_ID: str = Field(default="1112199003401971")
    INSTAGRAM_APP_SECRET: str = Field(default="33191e18dd0aa8db81049ee756d2f324")
    INSTAGRAM_ACCESS_TOKEN: str = Field(default="IGAAPzigKEbvNBZAE1pMG9uUTZAxR0NzSTRIdEE5SXNhc0hRMHVZAWWhsNjcxSzVUa2w1ZAHFyYmNoLVU3bXJvZA0N5YUdhWC1nN2V0WWtoSHJMS3ZAPTFB6am82SFZAwSG1uUXNJcU1hUDkxSFdVa2t4Tl9zbDNQcElTNGtkTmRVWkZADZAwZDZD")
    INSTAGRAM_ACCOUNT_ID: str = Field(default="17841451799717870")
    
    # Google Cloud Vision API settings
    GOOGLE_CLOUD_PROJECT: str = Field(default="deepshield-mvp")
    GOOGLE_APPLICATION_CREDENTIALS: str = Field(default="")
    
    # Translation API settings
    TRANSLATION_API_KEY: str = Field(default="")
    
    # Email settings
    SMTP_SERVER: str = Field(default="smtp.gmail.com")
    SMTP_PORT: int = Field(default=587)
    SMTP_USERNAME: str = Field(default="")
    SMTP_PASSWORD: str = Field(default="")
    FROM_EMAIL: str = Field(default="noreply@deepshield.ai")
    
    # SMS settings
    SMS_API_KEY: str = Field(default="")
    SMS_API_URL: str = Field(default="https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json")
    SMS_FROM_NUMBER: str = Field(default="")

    model_config = {
        "env_file": ".env",
        "extra": "allow"
    }

settings = Settings()
