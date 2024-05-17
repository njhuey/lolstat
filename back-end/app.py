from fastapi import FastAPI
from routers import stats

app = FastAPI()

app.include_router(stats.router, prefix="/stats", tags=["stats"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
