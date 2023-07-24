import datetime
from typing import List

from pydantic import BaseModel, Field

class PrizeDataItem(BaseModel):
    points: int
    count: int


class LotofacilModel(BaseModel):
    accumulated: bool = False
    date: str
    numbers: List[int]
    prizes_data: List[PrizeDataItem]
    last_draw: bool = False

class Lotofacil(LotofacilModel):
    id: str = Field(alias='_id')