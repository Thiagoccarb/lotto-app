from fastapi.routing import APIRouter

from schemas.lotofacil_schemas import LotofacilByNumbersResponse, LotofacilResponse, ValidateResponse
from controlllers.lotofacil_controller import LotofacilController


lotofacil_controller = LotofacilController()


lotofacil_router = APIRouter(prefix="/lotofacil", tags=["Lotofacil"])

lotofacil_router.add_api_route(
    "",
    lotofacil_controller.add,
    methods=["POST"],
    status_code=201,
    response_model=LotofacilResponse,
)

lotofacil_router.add_api_route(
    "/last",
    lotofacil_controller.get_last_result,
    methods=["GET"],
    status_code=200,
    response_model=LotofacilResponse,
)

lotofacil_router.add_api_route(
    "/numbers",
    lotofacil_controller.get_results_by_numbers,
    methods=["POST"],
    status_code=200,
    response_model=LotofacilByNumbersResponse,
)

lotofacil_router.add_api_route(
    "/validate",
    lotofacil_controller.validate,
    methods=["POST"],
    status_code=200,
    response_model=ValidateResponse,
)
