import uvicorn
from src.memorycloud.api import app
from src.memorycloud.config import settings

if __name__ == "__main__":
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
