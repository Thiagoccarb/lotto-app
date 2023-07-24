from abc import ABC, abstractmethod
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from database.create_db import db

from database.models.lotofacil_model import Lotofacil, LotofacilModel
  
  
class LotofacilRepository(ABC):

    @abstractmethod
    async def add(lotofacil_data: LotofacilModel) -> LotofacilModel:
            raise NotImplementedError
        
    @abstractmethod
    async def find_by_id(self, id: str) -> Lotofacil:
            raise NotImplementedError

class LotofacilRepositoryMongoDB(LotofacilRepository):

    def __init__(self):
        self.db = db

    async def add(self, lotofacil_data: LotofacilModel) -> Lotofacil:
        collection: AsyncIOMotorCollection = self.db["lotto"]
        item_data = lotofacil_data.model_dump()
        result = await collection.insert_one(item_data)
        new_data = await collection.find_one({"_id": result.inserted_id})
        new_data['_id'] = str(result.inserted_id)
        return Lotofacil(**new_data)
    
    async def find_by_id(self, id: str) -> Lotofacil:
        collection: AsyncIOMotorCollection = self.db["lotto"]
        document = await collection.find_one({"id": id})
        if document:
            return Lotofacil(**document)
        return None
