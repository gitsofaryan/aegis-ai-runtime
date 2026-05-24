import litellm
from core.config import settings
from core.logger import logger
import urllib.parse

def setup_cache():
    try:
        url = urllib.parse.urlparse(settings.REDIS_URL)
        host = url.hostname or "localhost"
        port = url.port or 6379
        password = url.password
        
        # Enable LiteLLM exact & semantic caching via Redis
        litellm.cache = litellm.Cache(
            type="redis", 
            host=host, 
            port=port, 
            password=password
        )
        logger.info(f"Cache layer configured at {host}:{port}.")
    except Exception as e:
        logger.error(f"Failed to setup cache: {e}")
