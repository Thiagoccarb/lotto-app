from database.create_db import db
from utils.logger import Logger

async def check_collection_existence():
    logger = Logger()
    logger.info('checking for existing collection')
    existing_collections = await db.list_collection_names()
    logger.info(f'collections available: {", ".join(existing_collections)}')
    collection_name = "lotofacil"
    if collection_name not in existing_collections:
        await db.create_collection(collection_name)
        logger.info('colection {} has been created'.format(collection_name))