from typing import Optional, Set

from pydantic import BaseModel, Field, HttpUrl


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
                "replace_url": "https://i.pixiv.cat",
            }
        }
