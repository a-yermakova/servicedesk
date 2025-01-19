from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str

    SMTP_HOST: str
    SMTP_PORT: int

    REDIS_PORT: int
    REDIS_HOST: str

    class Config:
        env_file = ".env"


settings = Settings()
