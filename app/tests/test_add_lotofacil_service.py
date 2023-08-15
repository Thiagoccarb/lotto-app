import unittest
from asynctest import CoroutineMock

from services.lotofacil_service.add_lotofacil_service import AddLotofacilService
from database.models.lotofacil_model import Lotofacil
from schemas.lotofacil_schemas import AddLotofacilRequest


class TestAddLotofacilService(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.lotofacil_repository = CoroutineMock()
        cls.lotofacil_repository.add = CoroutineMock()
    
    async def test_add_lotofacil_successfully(self):        
        service = AddLotofacilService(lotofacil_repository=self.lotofacil_repository)
        
        mock_request = AddLotofacilRequest(
            accumulated=False,
            date = '2023-01-01',
            numbers = [1,2,3,4,7,6,8,10,13,14,16,19,21,22,23,25],
            prizes_data = [
                {"points": 15, "count": 1},
                {"points": 14, "count": 1}, 
                {"points": 13, "count": 1},
                {"points": 12, "count": 1},
                {"points": 11, "count": 1},
            ],
            last_draw = False,
            id =1
        )
        
        self.lotofacil_repository.add.return_value = Lotofacil(**mock_request.model_dump())
        response = await service.execute(mock_request)

        self.lotofacil_repository.add.assert_called_once_with(mock_request)
        self.assertEqual(response.model_dump(), mock_request.model_dump())
