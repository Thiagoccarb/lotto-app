from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from utils.update_db import create_all_results_in_db
from utils.status_error import StatusError
from error_handlers.status_error_handler import handle_status_error_exception
from error_handlers.validation_error_handler import handle_validation_error
from database.create_collection import check_collection_existence
from routes import app_router

app = FastAPI(
    routes=app_router.routes,
    docs_url="/docs",
    on_startup=[check_collection_existence, create_all_results_in_db]
)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await handle_validation_error(request, exc)

@app.exception_handler(StatusError)
async def handle_exception(_, exc: StatusError):
    return await handle_status_error_exception(exc)

app.add_middleware(GZipMiddleware, minimum_size=1000)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
