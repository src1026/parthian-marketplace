from fastapi import FastAPI
from .routers import router

app = FastAPI(title="API Gateway")

app.include_router(router)