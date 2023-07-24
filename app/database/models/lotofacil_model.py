import datetime
from typing import List, Optional

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
    id: int

class Lotofacil(LotofacilModel):
    _id: Optional[str] = Field(exclude = True)