from fastapi import FastAPI


app = FastAPI()


@app.get("/health-check")
async def read_main() -> dict:
    return {"healthCheck": "healthy"}
