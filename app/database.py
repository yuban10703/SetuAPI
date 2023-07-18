import asyncio
import re
from typing import List
import os
from fastapi.logger import logger
from motor.motor_asyncio import AsyncIOMotorClient

from schema import Setu


class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(os.getenv('mongodb'))
        self.client.get_io_loop = asyncio.get_event_loop
        self.database = self.client[os.getenv('database')]
        self.collection = self.database[os.getenv('collection')]
        self.Flag = None


DB = Database()


def get_setu_cursor(r18: int, num: int, tags: set):
    condition = {
        "$and": [{"r18": {"$nin": [None]}}, {"delete": False}] if r18 == 2 else [{"r18": bool(r18)}, {"delete": False}]
    }
    for tag in tags:
        condition["$and"].append({"tags": {"$regex": re.compile(tag, re.I)}})
    return DB.collection.aggregate(
        [{"$match": condition}, {"$sample": {"size": num}}, {"$project": {"_id": 0, "delete": 0}}]
    )



async def get_setu_data(r18: int, num: int, tags: set, replace_url) -> List[Setu]:
    logger.info(f"r18:[{r18}] num:[{num}] tags:[{tags}] replace_url:[{replace_url}]")
    cursor = get_setu_cursor(r18, num, tags)
    if replace_url:
        setus = []
        async for setu in cursor:

            urls_dict: dict = setu["urls"]
            for url_quality, url in urls_dict.items():
                setu["urls"][url_quality] = url.replace(
                    "https://i.pximg.net", replace_url
                )
            setus.append(setu)
        return setus
    else:
        return await cursor.to_list(length=None)
