from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from services.llm_service import generate_response, stream_response
from services.firewall import check_prompt_injection
from services.router import route_request
from services.compression import compress_context
from services.rate_limiter import check_rate_limit

router = APIRouter(tags=["generation"])

class Message(BaseModel):
    role: str
    content: str

class GenerateRequest(BaseModel):
    model: str = "gpt-4o"
    messages: List[Message]
    stream: bool = False
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None

@router.post("/generate", dependencies=[Depends(check_rate_limit)])
async def generate_endpoint(req: GenerateRequest, request: Request):
    # Phase 2: Security - Prompt Injection Firewall
    check_prompt_injection(req.messages)
    
    # Phase 2: Context Compression
    compressed_messages = compress_context(req.messages, max_tokens=4000)
    
    # Phase 2: AI Router
    target_model = route_request(compressed_messages, req.model)
    
    if req.stream:
        from fastapi.responses import StreamingResponse
        return StreamingResponse(
            stream_response(target_model, compressed_messages, req.temperature, req.max_tokens),
            media_type="text/event-stream"
        )
    else:
        response = await generate_response(target_model, compressed_messages, req.temperature, req.max_tokens)
        return {"response": response}
