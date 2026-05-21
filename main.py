from fastapi import FastAPI

from routers.insights_router import insights_router

app = FastAPI()

app.include_router(insights_router)