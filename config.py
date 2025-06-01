from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    TOKEN: str
    BASE_URL: str
    API_MASTERS: str
    API_APPOINTMENTS: str
    API_BOOKING: str
    API_BOOK: str
    API_DELETE_BOOK: str

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
