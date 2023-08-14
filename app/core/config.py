import os
from pathlib import Path


class Setting:
    PRODUCTION_MODE: bool = False
    BACK_URL: str = 'http://localhost/'
    BACK_PORT: int = 8000
    C_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ROOT_DIR = os.path.dirname(os.path.abspath(C_PATH))
    FOLDER_DIR = Path(ROOT_DIR) / 'app'
    MONGO_DB_DATABASE_NAME: str = "Lia"
    MongoDB_URI = "mongodb://127.0.0.1:27017/" + MONGO_DB_DATABASE_NAME

Setting = Setting()
