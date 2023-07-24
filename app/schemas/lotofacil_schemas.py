from schemas.base_schemas import BaseResponse
from database.models.lotofacil_model import Lotofacil, LotofacilModel


class AddLotofacilRequest(LotofacilModel):
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "accumulated": False,
                "date": "2023-01-01",
                "numbers": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
                "prizes_data":[
                    {"points": 15, "count": 1},
                    {"points": 14, "count": 1}, 
                    {"points": 13, "count": 1},
                    {"points": 12, "count": 1},
                    {"points": 11, "count": 1},
                ],
                "last_draw": False,
            }
        }
    }

class LotofacilResponse(BaseResponse):
    result: Lotofacil