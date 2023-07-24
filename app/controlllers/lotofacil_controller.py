from fastapi import Depends

from services.lotofacil_service.get_last_result_service import GetResultsService
from services.lotofacil_service.add_lotofacil_service import AddLotofacilService
from schemas.lotofacil_schemas import AddLotofacilRequest, LotofacilResponse


class LotofacilController:
    
    async def add(
        self, 
        request: AddLotofacilRequest,
        add_lotofacil_service: AddLotofacilService = Depends(AddLotofacilService), 
    ) -> LotofacilResponse:
    
        data = await add_lotofacil_service.execute(request)
        return LotofacilResponse(success=True, message=None, status='ok', result=data)
    
    async def get_last_result(
        self, 
        get_results_service: GetResultsService = Depends(GetResultsService), 
    ) -> LotofacilResponse:
    
        data = await get_results_service.execute()
        return LotofacilResponse(success=True, message=None, status='ok', result=data)