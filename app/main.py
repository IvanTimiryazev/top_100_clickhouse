from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.api_v1.api import api_router


app = FastAPI(title="Test")
app.include_router(api_router)


@app.get("/", status_code=status.HTTP_200_OK)
def health() -> JSONResponse:
	return JSONResponse({"message": "It worked!!"})


if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT, log_level="debug")
