import os
import re

from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(os.getenv('mongodb'))
db = client[os.getenv('db')]
collection = db[os.getenv('col')]


async def find_setu(r18: int, num: int, tags: set):
    condition_and = []
    condition: dict = {} if r18 == 2 else {'r18': bool(r18)}
    for tag in tags:
        if not tag.isspace():  # tag不为空时
            condition_and.append({'tags': re.compile(tag.strip(), re.I)})
    if condition_and:
        condition["$and"] = condition_and
    return [
        data async for data in
        collection.aggregate([{'$match': condition}, {'$sample': {'size': num}}, {'$project': {'_id': 0}}])
    ]
