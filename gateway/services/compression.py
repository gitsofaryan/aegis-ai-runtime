from core.logger import logger

def compress_context(messages: list, max_tokens: int = 4000) -> list:
    """
    If the context exceeds max_tokens, summarize older messages or truncate.
    """
    total_chars = sum(len(msg.get("content", "")) if isinstance(msg, dict) else len(getattr(msg, "content", "")) for msg in messages)
    approx_tokens = total_chars / 4
    
    if approx_tokens > max_tokens:
        logger.info(f"Context size ({approx_tokens} tokens) exceeds {max_tokens}. Compressing...")
        compressed = []
        for msg in messages:
            role = msg.get("role") if isinstance(msg, dict) else getattr(msg, "role")
            if role == "system":
                compressed.append(msg)
        
        # Take the last 3 messages to reduce context window
        compressed.extend(messages[-3:])
        logger.info("Context compressed successfully.")
        return compressed
        
    return messages
