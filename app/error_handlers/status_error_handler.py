from fastapi.responses import JSONResponse

from utils.status_error import StatusError


async def handle_status_error_exception(exc: StatusError):
    error_response = {
        "success": False,
        "error": {"type": exc.status, "description": exc.message},
    }
    return JSONResponse(content=error_response, status_code=exc.status_code)
