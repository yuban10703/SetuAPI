import logging
from typing import Optional, Set

from fastapi import FastAPI, HTTPException, Query
from fastapi.logger import logger
from fastapi.responses import ORJSONResponse
from pydantic import HttpUrl

from database import get_setu_data
from schema import Item, Setu_out

gunicorn_logger = logging.getLogger("gunicorn.error")
logger.handlers = gunicorn_logger.handlers

if __name__ != "main":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)

app = FastAPI(
    title="setu", description="https://github.com/yuban10703/SetuAPI", version="0.1.5"
)


@app.get("/setu", response_model=Setu_out, response_class=ORJSONResponse)
async def setu_get(
        r18: Optional[int] = Query(0, ge=0, le=2),
        num: Optional[int] = Query(1, ge=1, le=50),
        tags: Set[str] = Query(set()),
        replace_url: Optional[HttpUrl] = None,
):
    filtered_tags = {tag.strip() for tag in tags if tag.strip()}
    setus = await get_setu_data(r18, num, filtered_tags, str(replace_url))
    if not setus:
        raise HTTPException(status_code=404, detail="色图库中没找到色图~")
    return {
        "detail": "",
        "count": len(setus),
        "tags": filtered_tags,
        "data": setus,
    }

@app.post("/setu", response_class=ORJSONResponse)
async def setu_post(item: Item):
    setus = await get_setu_data(item.r18, item.num, item.tags, str(item.replace_url))
    if not setus:
        raise HTTPException(status_code=404, detail="色图库中没找到色图~")
    return {
        "detail": "",
        "count": len(setus),
        "tags": item.tags,
        "data": setus,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=9999, reload=True)
