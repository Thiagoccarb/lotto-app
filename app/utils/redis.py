import json
from typing import Any
import aioredis


class RedisCache:
    def __init__(self, ttl_seconds: int = 60)-> None:
        self.redis = aioredis.from_url(
            "redis://:eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81@localhost:6379/0",
            encoding="utf-8",
            decode_responses=True
        )
        self.ttl = ttl_seconds
        
    async def set_value(self, key: str, data: Any):
        async with self.redis.client() as conn:
            if type(data) == str:
                await conn.set(key, data)
            elif type(data) in (set, list, dict):
                await conn.set(key, json.dumps(data))
            else:
                await conn.set(key, str(data))
                
            await conn.expire(key, self.ttl)  # Set the TTL after setting the value

          
    async def get_value(self, key: str, data: Any = None):
        async with self.redis.client() as conn:
          val = await conn.get(key)

          if val is None:
              await self.set_value(key, data)
              return data
          return val
