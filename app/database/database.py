import os

from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(os.getenv('mongodb'))
db = client[os.getenv('db')]
collection = db[os.getenv('col')]




async def find_setu(condition: dict, num: int):
    return [
        data async for data in
        collection.aggregate([{'$match': condition}, {'$sample': {'size': num}}, {'$project': {'_id': 0}}])
    ]
