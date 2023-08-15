from abc import ABC, abstractmethod
from typing import List
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
        
    @abstractmethod
    async def find_by_ids(self, ids: List[str]) -> List[Lotofacil]:
            raise NotImplementedError

    @abstractmethod
    async def batch_add(self, lotofacil_data_list: List[LotofacilModel]) -> List[Lotofacil]:
            raise NotImplementedError
        
    @abstractmethod
    async def find_all(self) -> List[Lotofacil]:
            raise NotImplementedError

class LotofacilRepositoryMongoDB(LotofacilRepository):

    def __init__(self):
        self.db = db

    async def add(self, lotofacil_data: LotofacilModel) -> Lotofacil:
        collection: AsyncIOMotorCollection = self.db["lotofacil"]
        item_data = lotofacil_data.model_dump()
        result = await collection.insert_one(item_data)
        new_data = await collection.find_one({"_id": result.inserted_id})
        del new_data['_id']
        return Lotofacil(**new_data)

    async def batch_add(self, lotofacil_data_list: List[LotofacilModel]) -> List[Lotofacil]:
        collection: AsyncIOMotorCollection = self.db["lotofacil"]
        await collection.insert_many([item.model_dump() for item in lotofacil_data_list])
        query = {"id": {"$in": [item.id for item in lotofacil_data_list]}}
        documents = await collection.find(query).to_list(None)
        
        for doc in documents:
            del doc['_id']
        
        lotofacil_list = [Lotofacil(**document) for document in documents]
        return lotofacil_list

    async def find_by_id(self, id: str) -> Lotofacil:
        collection: AsyncIOMotorCollection = self.db["lotofacil"]
        document = await collection.find_one({"id": id})
        if document:
            return Lotofacil(**document)
        return None

    async def find_by_ids(self, ids: List[str]) -> List[Lotofacil]:
        collection: AsyncIOMotorCollection = self.db["lotofacil"]
        query = {"id": {"$in": ids}}
        documents = await collection.find(query).to_list(None)

        lotofacil_list = [Lotofacil(**document) for document in documents]
        return lotofacil_list

    async def get_all_ids(self) -> List[str]:
        collection: AsyncIOMotorCollection = self.db["lotofacil"]

        # The aggregation pipeline to project only the 'id' field
        pipeline = [
            {"$project": {"_id": 0, "id": 1}}
        ]

        # Execute the aggregation pipeline and fetch the results
        cursor = collection.aggregate(pipeline)

        # Extract 'id' fields from the documents and put them in a list
        ids = [document["id"] async for document in cursor]

        return ids
    
    async def find_all(self) -> List[Lotofacil]:
        collection: AsyncIOMotorCollection = self.db["lotofacil"]
        documents = await collection.find({}).to_list(None)
        lotofacil_list = [Lotofacil(**document) for document in documents]
        return lotofacil_list