import cachetools
from typing import Any, Callable, Dict
from datetime import timedelta


global cached_objects
cached_objects = cachetools.TTLCache(10, 60)
persistent_cached_objects = cachetools.LRUCache(10)

class CacheRepository:
    def _set_ttl(self, ttl: int = None):
        global cached_objects
        
        if ttl and cached_objects.ttl != ttl:
            cached_objects = cachetools.TTLCache(10, ttl)
            
    def _cached_name(self, function: Callable, arguments: Any):
        return f'{str(function.__qualname__)}.{str(arguments)}'
    
    async def _async_add_to_cache(self, function: Callable, arguments: Any):

        cached_value = await function(**arguments)

        cached_objects.setdefault(f'{self._cached_name(function, arguments)}', cached_value)
        
    async def async_get_from_cache(self, function: Callable, arguments: Dict[str, Any] = {}, ttl: int = None):
        
        global cached_objects
        if ttl and cached_objects.ttl != ttl:
            self._set_ttl(ttl=ttl)
        cached_response = cached_objects.get(self._cached_name(function, arguments))
        
        if cached_response is None:
            await self._async_add_to_cache(function, arguments)
            
        return cached_objects.get(self._cached_name(function, arguments))
        
    def refresh(self):
        global cached_objects
        cached_objects.clear()