from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_hostname_port: int
    database_name: str
    database_username: str
    database_password: str
    secret_key: str
    algorithm : str
    access_token_expire_minutes: int
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # case_sensitive = True
    

settings=Settings()