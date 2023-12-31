import asyncio
from typing import List
from fastapi.params import Depends

from database.models.lotofacil_model import Lotofacil as Lf, LotofacilModel
from database.repositories.lotofacil_repository import LotofacilRepository, LotofacilRepositoryMongoDB
from utils.lotofacil import Lotofacil


class GetResultsByNumbersService:

    def __init__(
        self, 
        lotofacil: Lotofacil = Depends(Lotofacil),
        lotofacil_repository: LotofacilRepository = Depends(LotofacilRepositoryMongoDB)    
    ):
        self.lotofacil = lotofacil
        self.lotofacil_repository = lotofacil_repository
        
    async def _get_results_by_number(self, number: int):
        data = await self.lotofacil.get_results_by_number(number)
        return self.lotofacil.create_report(data)
    
    async def execute(
        self, 
        numbers: List[int] = [],
    ) -> List[Lotofacil]:
        existing_results = await self.lotofacil_repository.find_by_ids(numbers)
        existing_results_ids = {item.id for item in existing_results}

        results_numbers_to_get = [number for number in numbers if number not in existing_results_ids]
        
        if results_numbers_to_get:
            tasks = [self._get_results_by_number(number) for number in results_numbers_to_get]
            results = await asyncio.gather(*tasks)
            data = await self.lotofacil_repository.batch_add([LotofacilModel(**result) for result in results])
            existing_results = [ *existing_results, *data]
        # ids = await self.lotofacil_repository.get_all_ids()
        return existing_results

