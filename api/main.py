import re
from typing import Optional, Set

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel, Field

from database import DataBase

db = DataBase()


class Item(BaseModel):
    r18: Optional[bool] = False
    num: Optional[int] = Field(1, ge=1, le=30)
    tags: Set[str] = set()


app = FastAPI(
    title="setu",
    description="emmm",
    version="0.1.0",
    # openapi_url="/api/data_manger.json",
    # docs_url="/api/docs",
    # redoc_url="/api/redoc"
)


@app.get('/setu', response_class=ORJSONResponse)
async def setu_get(r18: bool = False,
                   num: int = Query(1, ge=1, le=30),
                   tags: Set[str] = Query(set())):
    condition = {'r18': r18}
    condition_and = []
    for tag in tags:
        if not tag.isspace():  # tag不为空时
            condition_and.append({'tags': re.compile(tag.strip(), re.I)})
    if condition_and:
        condition['$and'] = condition_and
    setus = await db.find(condition, num)
    if not setus:
        raise HTTPException(status_code=404, detail="色图库中没找到色图~")
    return {'code': 200, 'count': len(setus), 'tags': [i['tags'].pattern for i in condition_and], 'data': setus}


@app.post("/setu", response_class=ORJSONResponse)
async def setu_post(item: Item):
    condition = {'r18': item.r18}
    condition_and = []
    for tag in item.tags:
        if not tag.isspace():  # tag不为空时
            condition_and.append({'tags': re.compile(tag.strip(), re.I)})
    if condition_and:
        condition['$and'] = condition_and
    setus = await db.find(condition, item.num)
    if not setus:
        raise HTTPException(status_code=404, detail="色图库中没找到色图~")
    return {'code': 200, 'count': len(setus), 'tags': [i['tags'].pattern for i in condition_and], 'data': setus}


@app.get('/')
async def hello():
    return {'message': 'Hello world!'}


app.add_event_handler("startup", db.connect_db)
app.add_event_handler("shutdown", db.close_db)

# if __name__ == '__main__':
#     import uvicorn
#
#     uvicorn.run('main:app', host="0.0.0.0", port=80, reload=True)
