from fastapi.params import Depends

from schemas.lotofacil_schemas import AddLotofacilRequest
from database.repositories.lotofacil_repository import LotofacilRepository, LotofacilRepositoryMongoDB
from database.models.lotofacil_model import Lotofacil

class AddLotofacilService:

    def __init__(
        self, 
        lotofacil_repository: LotofacilRepository = Depends(LotofacilRepositoryMongoDB)
    ):
        self.lotofacil_repository = lotofacil_repository


    async def execute(self, data: AddLotofacilRequest) -> Lotofacil:
        return await self.lotofacil_repository.add(data)