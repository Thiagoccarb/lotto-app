from database.create_db import db
from utils.logger import Logger

async def check_collection_existence():
    logger = Logger()
    existing_collections = await db.list_collection_names()
    logger.info('checking for existing collection')
    target_collection_name = "lotto"
    if target_collection_name not in existing_collections:
        logger.info('checking for existing collection')
        await db.create_collection(target_collection_name)