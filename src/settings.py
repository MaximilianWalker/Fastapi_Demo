from typing import Set
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_name: str
    api_host: str
    api_port: int
    api_allowed_origins: Set[str]
    api_debug_mode: bool
    api_storage_path: str
    api_stream_chunk_size: int
    api_video_formats: Set[str]
    api_image_formats: Set[str]

    api_token_algorithm: str

    api_access_token_key: str
    api_access_token_expiration_time: int
    
    api_refresh_token_key: str
    api_refresh_token_expiration_time: int

    db_host: str
    db_port: int
    db_schema: str
    db_user: str
    db_password: str

    class Config:
        env_file = ".env"

settings = Settings()
