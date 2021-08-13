import os
import re
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient

from app.model import Setu

client = AsyncIOMotorClient(os.getenv('mongodb'))
db = client[os.getenv('db')]
collection = db[os.getenv('col')]


async def find_setu(r18: int, num: int, tags: set) -> List[Setu]:
    condition = {"$and": [{'r18': {'$nin': [None]}}] if r18 == 2 else [{'r18': bool(r18)}]}
    for tag in tags:
        if not tag.isspace():  # tag不为空时
            # noinspection PyTypeChecker
            condition["$and"].append({'tags': re.compile(tag.strip(), re.I)})
    return [
        data async for data in
        collection.aggregate([{'$match': condition}, {'$sample': {'size': num}}, {'$project': {'_id': 0}}])
    ]
