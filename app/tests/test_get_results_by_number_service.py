import unittest
from asynctest import CoroutineMock

from services.lotofacil_service.get_results_by_numbers_service import GetResultsByNumbersService
from services.lotofacil_service.get_last_result_service import GetResultsService
from database.models.lotofacil_model import LotofacilModel, Lotofacil


class TestGetResultsByNumbersService(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.lotofacil = CoroutineMock()
        cls.lotofacil_repository = CoroutineMock()

    async def test_with_a_list_of_non_existing_ids_in_db(self):        
        self.lotofacil_repository.find_by_ids = CoroutineMock()
        self.lotofacil_repository.batch_add = CoroutineMock()

        service = GetResultsByNumbersService(lotofacil = self.lotofacil, lotofacil_repository=self.lotofacil_repository)
        
        mock_numbers = [1,2]
        service._get_results_by_number = CoroutineMock()
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
       
        service._get_results_by_number.return_value = mock_data

        self.lotofacil_repository.find_by_ids.return_value = [Lotofacil(
          **mock_data
        )]

        results = await service.execute(mock_numbers)
        self.lotofacil_repository.find_by_ids.assert_called_once_with(mock_numbers)
        self.lotofacil_repository.batch_add.assert_called_once_with([LotofacilModel(**result.dict()) for result in results])