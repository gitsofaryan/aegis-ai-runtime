Write-Host "Starting Docker Compose services..."
docker-compose up -d

Write-Host "Activating Python Virtual Environment and Starting FastAPI Server..."
cd gateway
if (-Not (Test-Path ".venv")) {
    Write-Host "Virtual environment not found, creating one..."
    uv venv .venv
    .venv\Scripts\activate
    uv pip install -r requirements.txt
} else {
    .venv\Scripts\activate
}

Write-Host "Running Aegis AI Gateway on http://localhost:8000"
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
