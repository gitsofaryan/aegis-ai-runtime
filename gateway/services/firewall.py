import re
from fastapi import HTTPException
from core.logger import logger

# Basic heuristic list for MVP
FORBIDDEN_PATTERNS = [
    r"(?i)ignore\s+(all\s+)?(previous\s+)?(instructions|directions)",
    r"(?i)system\s+prompt",
    r"(?i)you\s+are\s+now",
    r"(?i)bypass",
    r"(?i)jailbreak",
]

def check_prompt_injection(messages: list) -> bool:
    """
    Returns True if an injection is detected, else False.
    Raises HTTPException if blocked directly.
    """
    for msg in messages:
        if hasattr(msg, "role") and msg.role == "user":
            content = getattr(msg, "content", "")
        elif isinstance(msg, dict) and msg.get("role") == "user":
            content = msg.get("content", "")
        else:
            continue
            
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, content):
                logger.warning(f"Prompt Injection Blocked! Pattern matched: {pattern}")
                raise HTTPException(status_code=400, detail="Prompt blocked by security firewall.")
    
    return False
