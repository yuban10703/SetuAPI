from typing import Optional, Set

from pydantic import BaseModel, Field


class Item(BaseModel):
    r18: Optional[bool] = False
    num: Optional[int] = Field(1, ge=1, le=30)
    tags: Set[str] = set()
