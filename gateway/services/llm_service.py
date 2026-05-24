import litellm
import json
from core.logger import logger
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def generate_response(model: str, messages: list, temperature: float = 0.7, max_tokens: int = None):
    logger.info(f"Generating response using model: {model}")
    try:
        # LiteLLM standardizes the completion call
        response = await litellm.acompletion(
            model=model,
            messages=[m.model_dump() for m in messages],
            temperature=temperature,
            max_tokens=max_tokens
        )
        logger.info("Generation successful")
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise e

async def stream_response(model: str, messages: list, temperature: float = 0.7, max_tokens: int = None):
    logger.info(f"Streaming response using model: {model}")
    try:
        response_stream = await litellm.acompletion(
            model=model,
            messages=[m.model_dump() for m in messages],
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )
        async for chunk in response_stream:
            if chunk.choices[0].delta.content:
                yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"
        yield "data: [DONE]\n\n"
    except Exception as e:
        logger.error(f"Streaming failed: {e}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
