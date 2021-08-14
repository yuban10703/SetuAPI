from typing import List

from pydantic import BaseModel

from .setu_data import Setu


class Setu_out(BaseModel):
    detail: str = ''
    count: int
    tags: List[str]
    data: List[Setu]
