from fastapi import FastAPI

from gdelt_api.routers import relations_router

ROUTE_PREFIX = "/api/v1"

app = FastAPI()
app.include_router(relations_router.router, prefix=ROUTE_PREFIX)


@app.get("/health-check")
async def read_main() -> dict:
    return {"healthCheck": "healthy"}
