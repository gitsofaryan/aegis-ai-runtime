#!/bin/bash
echo "Starting Docker Compose services..."
docker-compose up -d

echo "Activating Python Virtual Environment and Starting FastAPI Server..."
cd gateway || exit
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found, creating one..."
    uv venv .venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
else
    source .venv/bin/activate
fi

echo "Running Aegis AI Gateway on http://localhost:8000"
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
