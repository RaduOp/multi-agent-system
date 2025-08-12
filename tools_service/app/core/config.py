from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Tools Service"
    debug: bool = True
    environment: str = "development"

    random_param: str = "a very random parameter"
    random_param_2: str = "even more random parameter"

    timeout: int = Field(10, ge=1, le=60)

    # Overwrite settings with local .env file
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
