from fastapi import APIRouter

from schemas.base_schemas import MissingFieldErrorSchema
from routes.lotofacil_routes import lotofacil_router


app_router = APIRouter(redirect_slashes=True)

app_router.include_router(
    lotofacil_router,
    responses={
        201: {
            "description": "data created",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "status": "ok",
                        "result": {
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
                            "id": 1
                        },
                    },
                }
            },
        },
        400: {
            "description": "missing_field",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": {
                            "type": "missing_field",
                            "description": f"missing field `field_name`",
                        },
                    },
                }
            },
        },
        422: {
            "description": "status not returned",
        },
        500: {
            "description": "missing_field",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": {
                            "type": "internal error",
                            "description": "Internal server error.",
                        },
                    },
                },        
            },
        }
    }
)

