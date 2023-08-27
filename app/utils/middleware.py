from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import ORJSONResponse

from utils.redis import RedisCache

class IpTrackerMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            redis: RedisCache = RedisCache(),
    ):
        self.redis = redis
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
    
        client_host = request.client.host
        client_ip_count_request = await self.redis.get_value(str(client_host))
        if client_ip_count_request:
            if int(client_ip_count_request) > 10:
                return ORJSONResponse(
                content={
                    'success': False,
                    'error': {
                      "type": "too_many_requests",
                        "description": "Ip banned due to too many requests.",
                    }   
                }, 
                status_code=429
            )
            client_ip_count_request =  int(client_ip_count_request) + 1
        else:
            client_ip_count_request = 1

        await self.redis.set_value(str(client_host), client_ip_count_request)
        return await call_next(request)
