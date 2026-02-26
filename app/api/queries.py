from fastapi import APIRouter

router = APIRouter(prefix="/api/queries", tags=["queries"])

@router.get("/")
async def get_queries():
    return {"message": "Queries endpoint"}