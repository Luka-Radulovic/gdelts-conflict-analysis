from fastapi import FastAPI

ROUTE_PREFIX = "/api/v1"

app = FastAPI()
@app.get("/healthcheck")
async def read_main() -> dict:
    return {"healthCheck": "healthy"}