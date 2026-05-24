import os
from fastapi.testclient import TestClient
from api.main import app
import litellm

# Setup mock for litellm to avoid making real API calls during test
async def mock_acompletion(*args, **kwargs):
    class MockDelta:
        content = " mock"
    class MockMessage:
        content = "This is a mock response from Aegis Gateway!"
    class MockChoice:
        delta = MockDelta()
        message = MockMessage()
    class MockResponse:
        choices = [MockChoice()]
        def get(self, key, default=None):
            if key == "usage":
                return {"prompt_tokens": 5, "completion_tokens": 10}
            return default
    
    if kwargs.get("stream"):
        async def stream_generator():
            yield MockResponse()
        return stream_generator()
    
    return MockResponse()

litellm.acompletion = mock_acompletion

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    print("Health check passed.")

def test_generate():
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello!"}],
        "stream": False
    }
    response = client.post("/api/v1/generate", json=payload)
    assert response.status_code == 200
    assert response.json()["response"] == "This is a mock response from Aegis Gateway!"
    print("Generate check passed.")

if __name__ == "__main__":
    print("Running Phase 1 tests...")
    test_health()
    test_generate()
    print("All Phase 1 tests passed successfully!")
