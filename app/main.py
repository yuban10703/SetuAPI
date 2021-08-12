import re
from typing import Set, Union

from fastapi import FastAPI, Query, HTTPException

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


@app.get('/setu', response_model=Setu_out)
async def setu_get(r18: Union[bool, None] = None,
                   num: int = Query(1, ge=1, le=30),
                   tags: Set[str] = Query(set())):
    condition: dict = {} if r18 is None else {'r18': r18}
    condition_and = []
    for tag in tags:
        if not tag.isspace():  # tag不为空时
            condition_and.append({'tags': re.compile(tag.strip(), re.I)})
    if condition_and:
        condition["$and"] = condition_and
    setus = await find_setu(condition, num)
    if not setus:
        raise HTTPException(status_code=404, detail="色图库中没找到色图~")
    return {'code': 200, 'count': len(setus), 'tags': [i['tags'].pattern for i in condition_and], 'data': setus}


@app.post("/setu", response_model=Setu_out)
async def setu_post(item: Item):
    condition: dict = {} if item.r18 is None else {'r18': item.r18}
    condition_and = []
    for tag in item.tags:
        if not tag.isspace():  # tag不为空时
            condition_and.append({'tags': re.compile(tag.strip(), re.I)})
    if condition_and:
        condition['$and'] = condition_and
    setus = await find_setu(condition, item.num)
    if not setus:
        raise HTTPException(status_code=404, detail="色图库中没找到色图~")
    return {'code': 200, 'count': len(setus), 'tags': [i['tags'].pattern for i in condition_and], 'data': setus}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=8080, reload=True)
