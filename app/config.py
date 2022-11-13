import os


class Settings:
    PORT = os.getenv("PORT", 5000)
    DEBUG_MODE = bool(os.getenv("DEBUG_MODE", False))
    VERSION = "0.23.1"

    PWD = os.getcwd()


settings = Settings()