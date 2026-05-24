from fastapi import FastAPI
from api.routers import generate
from core.config import settings
import uvicorn
from services.observability import setup_observability
from services.cache_service import setup_cache

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise AI Runtime Gateway",
    version="1.0.0"
)

# Setup Gateway layers
setup_observability()
setup_cache()

app.include_router(generate.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
