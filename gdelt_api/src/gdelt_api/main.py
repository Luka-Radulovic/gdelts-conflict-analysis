from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gdelt_api.routers import relations_router

ROUTE_PREFIX = "/api/v1"

app = FastAPI()
app.include_router(relations_router.router, prefix=ROUTE_PREFIX)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health-check")
async def read_main() -> dict:
    return {"healthCheck": "healthy"}
