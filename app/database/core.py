from fastapi.logger import logger
from motor.motor_asyncio import AsyncIOMotorClient


class Database:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.database = None
        self.collection = None

    async def connect(self, url, database, collection):
        self.client = AsyncIOMotorClient(url)
        self.database = self.client[database]
        self.collection = self.database[collection]
        logger.warning("connect success")

    async def close(self):
        self.client.close()
        logger.warning("closed")


database = Database()
