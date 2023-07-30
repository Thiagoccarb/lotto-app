import asyncio

from utils.logger import Logger
from services.lotofacil_service.get_last_result_service import GetResultsService
from services.lotofacil_service.get_results_by_numbers_service import GetResultsByNumbersService
from utils.lotofacil import Lotofacil
from database.repositories.lotofacil_repository import LotofacilRepositoryMongoDB


lotofacil = Lotofacil()
lotofacil_repository = LotofacilRepositoryMongoDB()
last_result_service = GetResultsService(lotofacil, lotofacil_repository)
results_service = GetResultsByNumbersService(lotofacil, lotofacil_repository)

async def create_all_results_in_db():
    logger = Logger()
    last_result_data = await last_result_service._get_last_result()
    last_result_data_id = last_result_data.get('id')
    ids = await lotofacil_repository.get_all_ids()
    missing_ids = [item for item in [n for n in range(1, int(last_result_data_id) + 1)] if not item in ids]
    if not missing_ids:
        return logger.info('Database already up to date')

    await results_service.execute(missing_ids)
    logger.info('Database has been updated with all results')

if __name__ == "__main__":
    asyncio.run(create_all_results_in_db())