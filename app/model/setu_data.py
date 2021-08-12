from datetime import datetime
from typing import List

from pydantic import BaseModel, HttpUrl


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

