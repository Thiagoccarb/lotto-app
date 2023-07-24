from typing import Optional
from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool
    message: Optional[str]
    status: str

class Error(BaseModel):
    type: str
    description: str 
    
class MissingFieldErrorSchema(BaseModel):
    success: bool
    error: Optional[Error]

    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "error": {
                    "type": "missing_field",
                    "description": f"missing field `field_name`",
                },
            }
        }