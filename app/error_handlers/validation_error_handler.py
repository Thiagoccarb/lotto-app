import re
from fastapi import Depends, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from utils.status_error import StatusError
from utils.logger import Logger

async def handle_validation_error(_: Request, exc: RequestValidationError, logger: Logger = Depends(Logger)):
    for error in exc.errors():
        print(error)
        try:
            msg = error["msg"]
            if msg == 'JSON decode error':
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "error": {
                        "type": "bad_request",
                        "description": "Invalid JSON request.",
                    },
                },
                )
            
            if "regex" in error["type"]:
                msgs = [error["msg"] for error in exc.errors()]
                fields = [field["loc"][1] for field in exc.errors()]
                description = [
                    item.replace("string", f"`{fields[i]}`")
                    for i, item in enumerate(msgs)
                ]
                description = ", ".join(description).replace('"', "").rstrip(", ")
                return JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    content={
                        "success": False,
                        "error": {
                            "type": "unprocessable_entity",
                            "description": description,
                        },
                    },
                )
            if msg == "Field required":
                fields = ",".join(
                    [str("`" + error["loc"][1] + "`") for error in exc.errors()]
                )

                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "success": False,
                        "error": {
                            "type": "missing_field",
                            "description": f"missing {fields}",
                        },
                    },
                )
        except IndexError:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "error": {
                        "type": "missing_field",
                        "description": f"missing body request",
                    },
                },
            )
        except StatusError as e:
            logger.error(e)
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "success": False,
                    "error": {"type": e.status, "description": e.message},
                },
            )
        except Exception as e:
            logger.error(e)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "error": {
                        "type": "internal error",
                        "description": "Internal server error.",
                    },
                },
            )
