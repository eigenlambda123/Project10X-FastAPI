import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("uvicorn.access")

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log request and response details
    including client IP, method, URL, status code, and duration.
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = round(time.time() - start_time, 4)

        client_ip = request.client.host
        method = request.method
        url = str(request.url)
        status_code = response.status_code

        logger.info(
            f"{client_ip} | {method} {url} | {status_code} | {duration}s"
        )
        return response
