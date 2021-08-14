import logging
from typing import Set, Optional

from fastapi import FastAPI, Query, HTTPException
from fastapi.logger import logger
from fastapi.responses import ORJSONResponse

from app.database import find_setu
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
    version="0.1.1"
)


@app.get('/setu', response_model=Setu_out, response_class=ORJSONResponse)
async def setu_get(r18: Optional[int] = Query(0, ge=0, le=2),
                   num: Optional[int] = Query(1, ge=1, le=30),
                   tags: Set[str] = Query(set())):
    logger.info('r18:[{r18}] num:[{num}] tags:[{tags}]'.format(tags=tags, r18=r18, num=num))
    setus = await find_setu(r18, num, tags)
    if not setus:
        raise HTTPException(status_code=404, detail="色图库中没找到色图~")
    return {'detail': '', 'count': len(setus), 'tags': [tag for tag in tags if not tag.isspace()], 'data': setus}


@app.post("/setu", response_model=Setu_out, response_class=ORJSONResponse)
async def setu_post(item: Item):
    logger.info('r18:[{r18}] num:[{num}] tags:[{tags}]'.format(tags=item.tags, r18=item.r18, num=item.num))
    setus = await find_setu(item.r18, item.num, item.tags)
    if not setus:
        raise HTTPException(status_code=404, detail="色图库中没找到色图~")
    return {'detail': '', 'count': len(setus), 'tags': [tag for tag in item.tags if not tag.isspace()], 'data': setus}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=8080, reload=True)
