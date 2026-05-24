import litellm
from core.logger import logger

def setup_observability():
    def log_success(kwargs, completion_response, start_time, end_time):
        try:
            latency = (end_time - start_time).total_seconds()
            model = kwargs.get("model", "unknown")
            try:
                cost = litellm.completion_cost(completion_response)
            except Exception:
                cost = 0.0

            usage = completion_response.get("usage", {})
            if isinstance(usage, dict):
                prompt_tokens = usage.get("prompt_tokens", 0)
                completion_tokens = usage.get("completion_tokens", 0)
            else:
                # LiteLLM sometimes returns object instead of dict
                prompt_tokens = getattr(usage, "prompt_tokens", 0)
                completion_tokens = getattr(usage, "completion_tokens", 0)
            
            # Check if this was a cache hit
            is_cache_hit = kwargs.get("cache_hit", False)
            cache_str = "[CACHE HIT]" if is_cache_hit else ""

            logger.info(
                f"SUCCESS {cache_str} | Model: {model} | Latency: {latency:.2f}s | "
                f"Tokens: {prompt_tokens} in / {completion_tokens} out | Cost: ${cost:.6f}"
            )
        except Exception as e:
            logger.error(f"Error in success callback: {e}")

    def log_failure(kwargs, completion_response, start_time, end_time):
        model = kwargs.get("model", "unknown")
        exception = kwargs.get("exception", "Unknown error")
        logger.error(f"FAILURE | Model: {model} | Error: {str(exception)}")

    litellm.success_callback = [log_success]
    litellm.failure_callback = [log_failure]
    logger.info("Observability layer configured.")
