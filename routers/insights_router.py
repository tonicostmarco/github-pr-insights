from fastapi import APIRouter

from services import analytics_service

insights_router = APIRouter(prefix="/insights", tags=["insights"])

@insights_router.get("/")
async def insights(date_from, date_to):

    response = analytics_service.init(date_from, date_to)

    return {"status": "ok", "result": response}