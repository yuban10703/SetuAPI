import re
from typing import List

from fastapi.logger import logger

from app.model import Setu
from .core import database


def get_setu_cursor(r18: int, num: int, tags: set):
    condition = {"$and": [{'r18': {'$nin': [None]}}] if r18 == 2 else [{'r18': bool(r18)}]}
    for tag in tags:
        if not tag.isspace() and len(tag) != 0:  # tag不为空时
            # noinspection PyTypeChecker
            condition["$and"].append({'tags': re.compile(tag.strip(), re.I)})

    return database.collection.aggregate(
        [
            {'$match': condition},
            {'$sample': {'size': num}},
            {'$project': {'_id': 0}}
        ]
    )


async def get_setu_data(r18: int, num: int, tags: set, replace_url) -> List[Setu]:
    logger.info(f'r18:[{r18}] num:[{num}] tags:[{tags}] replace_url:[{replace_url}]')
    cursor = get_setu_cursor(r18, num, tags)
    if replace_url:
        setus = []
        async for setu in cursor:
            urls_dict: dict = setu['urls']
            for url_quality, url in urls_dict.items():
                setu['urls'][url_quality] = url.replace("https://i.pximg.net", replace_url)
            setus.append(setu)
        return setus
    else:
        return await cursor.to_list(length=None)
