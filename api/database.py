import os

from motor.motor_asyncio import AsyncIOMotorClient


class DataBase:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

    async def connect_db(self):
        """Create database connection."""
        client = AsyncIOMotorClient(os.getenv('mongodb'))
        self.db = client[os.getenv('db')]
        self.collection = self.db[os.getenv('col')]

    async def close_db(self):
        """Close database connection."""
        self.client.close()

    async def find(self, condition: dict, num: int):
        return [
            data async for data in
            self.collection.aggregate([{'$match': condition}, {'$sample': {'size': num}}, {'$project': {'_id': 0}}])
        ]


