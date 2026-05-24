from core.logger import logger

def route_request(messages: list, requested_model: str) -> str:
    """
    Routes to a cheaper model if the prompt is very simple.
    Otherwise uses the requested model (or default advanced model).
    """
    content = ""
    for msg in messages:
        if isinstance(msg, dict) and msg.get("role") == "user":
            content += msg.get("content", "")
        elif hasattr(msg, "role") and msg.role == "user":
            content += getattr(msg, "content", "")
            
    word_count = len(content.split())
    # If the user is just saying a short greeting or phrase
    if word_count < 10 and "solve" not in content.lower() and "code" not in content.lower():
        routed_model = "gpt-3.5-turbo"
        logger.info(f"AI Router: Routing simple prompt to {routed_model}")
        return routed_model
        
    logger.info(f"AI Router: Routing complex prompt to {requested_model}")
    return requested_model
