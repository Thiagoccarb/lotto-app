import asyncio
from typing import List
from fastapi.params import Depends

from database.models.lotofacil_model import LotofacilModel
from database.repositories.lotofacil_repository import LotofacilRepository, LotofacilRepositoryMongoDB
from utils.lotofacil import Lotofacil


class GetResultsService:

    def __init__(
        self, 
        lotofacil: Lotofacil = Depends(Lotofacil),
        lotofacil_repository: LotofacilRepository = Depends(LotofacilRepositoryMongoDB)    
    ):
        self.lotofacil = lotofacil
        self.lotofacil_repository = lotofacil_repository
        
    async def _get_last_result(self):
        data =  await self.lotofacil.get_last_result()
        return self.lotofacil.create_report(data)

    async def execute(
        self, 
    ) -> Lotofacil:
        data = await self._get_last_result()
        result_id = data.get('id')
        existing_result = await self.lotofacil_repository.find_by_id(result_id)
        
        if not existing_result:
            new_result = await self.lotofacil_repository.add(LotofacilModel(**data))
            return new_result

        return existing_result
        
