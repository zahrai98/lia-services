import motor.motor_asyncio
from beanie import init_beanie

from app.core.config import Setting
from product.model.product_dao import ProductDao


class Database:
    MOTOR_CLIENT = None
    DATABASE = None

    @classmethod
    async def init_db(cls):
        try:
            cls.MOTOR_CLIENT = motor.motor_asyncio.AsyncIOMotorClient()
            cls.DATABASE = cls.MOTOR_CLIENT[Setting.MONGO_DB_DATABASE_NAME]
            document_models = [ProductDao.Product]
            await init_beanie(database=cls.DATABASE, document_models=document_models, allow_index_dropping=True)
        except Exception as e:
            print(e)
            raise e
