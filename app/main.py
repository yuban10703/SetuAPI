import logging
import os
from typing import Set, Optional

from fastapi import FastAPI, Query, HTTPException
from fastapi.logger import logger
from fastapi.responses import ORJSONResponse
from pydantic import HttpUrl

from app.database import database, get_setu_data
from app.model import Item, Setu_out

gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers

if __name__ != "main":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)

app = FastAPI(
    title="setu",
    description="https://github.com/yuban10703/SetuAPI",
    version="0.1.4"
)


@app.on_event("startup")
async def on_app_start():
    await database.connect(os.getenv('mongodb'), os.getenv('db'), os.getenv('col'))


@app.on_event("shutdown")
async def on_app_shutdown():
    await database.close()


@app.get('/setu', response_model=Setu_out, response_class=ORJSONResponse)
async def setu_get(
        r18: Optional[int] = Query(0, ge=0, le=2),
        num: Optional[int] = Query(1, ge=1, le=30),
        tags: Set[str] = Query(set()),
        replace_url: Optional[HttpUrl] = None):
    setus = await get_setu_data(r18, num, tags, replace_url)
    if not setus:
        raise HTTPException(status_code=404, detail="色图库中没找到色图~")
    return {'detail': '', 'count': len(setus), 'tags': [tag for tag in tags if not tag.isspace() and len(tag) != 0],
            'data': setus}


@app.post("/setu", response_model=Setu_out, response_class=ORJSONResponse)
async def setu_post(item: Item):
    setus = await get_setu_data(item.r18, item.num, item.tags, item.replace_url)
    if not setus:
        raise HTTPException(status_code=404, detail="色图库中没找到色图~")
    return {'detail': '', 'count': len(setus),
            'tags': [tag for tag in item.tags if not tag.isspace() and len(tag) != 0], 'data': setus}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=8080, reload=True)
