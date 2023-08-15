import unittest
from asynctest import CoroutineMock

from schemas.lotofacil_schemas import LotofacilByNumbersRequest
from services.lotofacil_service.validate_service import ValidateService
from database.models.lotofacil_model import Lotofacil


class TestValidateService(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.lotofacil_repository = CoroutineMock()
        cls.cache_repository = CoroutineMock()

    async def test_a_valid_lotofacil_set_of_numbers(self):
        mock_data =  {
            'accumulated': False,
            'date': '29/09/2003', 
            'numbers': ['02', '03', '05', '06', '09', '10', '11', '13', '14', '16', '18', '20', '23', '24', '25'], 
            'prizes_data': [
                {'points': 15, 'count': 5}, 
                {'points': 14, 'count': 154},
                {'points': 13, 'count': 4645}, 
                {'points': 12, 'count': 48807}, 
                {'points': 11, 'count': 257593}], 
            'id': 1, 
            'last_draw': True
        }        
        self.lotofacil_repository.find_all = CoroutineMock() 
        mock_results = [Lotofacil(**mock_data)]
        self.cache_repository.async_get_from_cache = CoroutineMock(
          return_value = mock_results
        )

        service = ValidateService(lotofacil_repository = self.lotofacil_repository, cache_repository=self.cache_repository)
        results = await service.execute(numbers=LotofacilByNumbersRequest(numbers= [1,2,3,4,7,6,8,10,13,14,16,19,21,22,23,25]))
        self.cache_repository.async_get_from_cache.assert_called_once_with(self.lotofacil_repository.find_all)