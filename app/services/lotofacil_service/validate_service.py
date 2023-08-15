from fastapi.params import Depends

from utils.cache import CacheRepository
from schemas.lotofacil_schemas import LotofacilByNumbersRequest
from database.repositories.lotofacil_repository import LotofacilRepository, LotofacilRepositoryMongoDB


class ValidateService:

    def __init__(
        self, 
        lotofacil_repository: LotofacilRepository = Depends(LotofacilRepositoryMongoDB),
        cache_repository: CacheRepository = Depends(CacheRepository),
    ):
        self.lotofacil_repository = lotofacil_repository
        self.cache_repository = cache_repository

    async def execute(
        self, 
        numbers: LotofacilByNumbersRequest
    ):
        report = []
        
        results = await self.cache_repository.async_get_from_cache(self.lotofacil_repository.find_all) 
        for result in results:
            data = {}
            points = len([number for number in numbers if number in result.numbers])
            if points >= 15 and points <= 20:
                data['id'] = result.id
                data['points'] = points        
                report.append(data)
        return report

