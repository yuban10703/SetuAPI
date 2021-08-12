from typing import Optional, Set, Union

from pydantic import BaseModel, Field


class Item(BaseModel):
    r18: Union[bool, None] = None
    num: Optional[int] = Field(1, ge=1, le=30)
    tags: Set[str] = set()
