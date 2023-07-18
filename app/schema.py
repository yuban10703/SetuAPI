from datetime import datetime
from typing import Optional, Set, List

from pydantic import Field, HttpUrl, BaseModel, validator


class Url(BaseModel):
    original: HttpUrl
    large: HttpUrl
    medium: HttpUrl


class Artwork(BaseModel):
    title: str
    id: int


class Author(BaseModel):
    name: str
    id: int


class Size(BaseModel):
    width: int
    height: int


class Setu(BaseModel):
    artwork: Artwork
    author: Author
    sanity_level: int
    r18: bool
    page: int
    create_date: datetime
    size: Size
    tags: List[str]
    urls: Url


class Item(BaseModel):
    r18: Optional[int] = Field(0, ge=0, le=2)
    num: Optional[int] = Field(1, ge=1, le=50)
    tags: Set[str] = set()
    replace_url: Optional[HttpUrl] = None

    class Config:
        schema_extra = {
            "example": {
                "r18": "0",
                "num": "1",
                "tags": [],
                "replace_url": "https://i.pixiv.re",
            }
        }

    @validator('tags', pre=True)
    def remove_empty_tags(cls, tags):
        return {tag.strip() for tag in tags if tag.strip()}


class Setu_out(BaseModel):
    detail: str = ''
    count: int
    tags: List[str]
    data: List[Setu]
