from typing import Set, Optional

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import ORJSONResponse

from .database import find_setu
from .model import Item, Setu_out

app = FastAPI(
    title="setu",
    description="emmm",
    version="0.1.0",
    # openapi_url="/fastapi/data_manger.json",
    # docs_url="/fastapi/docs",
    # redoc_url="/fastapi/redoc"
)


@app.get('/setu', response_model=Setu_out, response_class=ORJSONResponse)
async def setu_get(r18: Optional[int] = Query(0, ge=0, le=2),
                   num: Optional[int] = Query(1, ge=1, le=30),
                   tags: Set[str] = Query(set())):
    setus = await find_setu(r18, num, tags)
    if not setus:
        raise HTTPException(status_code=404, detail="色图库中没找到色图~")
    return {'code': 200, 'count': len(setus), 'tags': [tag for tag in tags if not tag.isspace()], 'data': setus}


@app.post("/setu", response_model=Setu_out, response_class=ORJSONResponse)
async def setu_post(item: Item):
    setus = await find_setu(item.r18, item.num, item.tags)
    if not setus:
        raise HTTPException(status_code=404, detail="色图库中没找到色图~")
    return {'code': 200, 'count': len(setus), 'tags': [tag for tag in item.tags if not tag.isspace()], 'data': setus}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=8080, reload=True)
