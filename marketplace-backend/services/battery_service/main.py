from fastapi import FastAPI
from .routers import router

app = FastAPI(title="Battery Marketplace API")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Battery Marketplace API is running!"}
