import time
from fastapi import HTTPException, Request
from redis.asyncio import Redis
from core.config import settings

redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)

async def check_rate_limit(request: Request):
    """
    Basic fixed window rate limiter: max 50 requests per minute per IP.
    """
    client_ip = request.client.host if request.client else "unknown"
    window = int(time.time() / 60)
    key = f"rate_limit:{client_ip}:{window}"
    
    try:
        current_count = await redis_client.incr(key)
        if current_count == 1:
            await redis_client.expire(key, 65)
            
        if current_count > 50:
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    except Exception as e:
        # If redis fails, fail open to avoid downtime, or log it
        pass
        
    return True
