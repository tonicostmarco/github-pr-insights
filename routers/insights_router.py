from fastapi import APIRouter

from services import analytics_service
from fastapi import Header

insights_router = APIRouter(prefix="/insights", tags=["insights"])

@insights_router.get("/")
async def insights(date_from, date_to, authorization: str = Header(None)):
    if authorization is None:
        return {"status": "Unauthorized", "result": []}
    else:
        token = authorization.split(" ")[1]

        response = analytics_service.init(date_from, date_to, token)

        return {"status": "ok", "result": response}