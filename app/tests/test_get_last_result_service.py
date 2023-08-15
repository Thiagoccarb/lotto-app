import unittest
from unittest.mock import Mock
from asynctest import CoroutineMock

from services.lotofacil_service.get_last_result_service import GetResultsService
from database.models.lotofacil_model import LotofacilModel, Lotofacil


class TestGetResultsService(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.lotofacil = CoroutineMock()
        cls.lotofacil_repository = CoroutineMock()

    async def test_get_last_non_existing_result(self):        
        self.lotofacil_repository.find_by_id = CoroutineMock()
        self.lotofacil_repository.add = CoroutineMock()

        service = GetResultsService(lotofacil = self.lotofacil, lotofacil_repository=self.lotofacil_repository)
        
        mock_last_result = 1
        service._get_last_result = CoroutineMock()
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
       
        service._get_last_result.return_value = mock_data
        
        self.lotofacil_repository.find_by_id.return_value = None
        self.lotofacil_repository.add.return_value = CoroutineMock()

        await service.execute()

        self.lotofacil_repository.find_by_id.assert_called_once_with(mock_last_result)
        self.lotofacil_repository.add.assert_called_once_with(LotofacilModel(**mock_data))
        
    async def test_get_last_with_existing_result(self):        
        self.lotofacil_repository.find_by_id = CoroutineMock()
        self.lotofacil_repository.add = CoroutineMock()

        service = GetResultsService(lotofacil = self.lotofacil, lotofacil_repository=self.lotofacil_repository)
        
        mock_last_result = 1
        service._get_last_result = CoroutineMock()
        
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
       
        service._get_last_result.return_value = mock_data
        
        self.lotofacil_repository.find_by_id.return_value = Lotofacil(**mock_data)

        await service.execute()

        self.lotofacil_repository.find_by_id.assert_called_once_with(mock_last_result)
        self.lotofacil_repository.add.assert_not_called()