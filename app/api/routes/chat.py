from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def create_chat():
    return {"status": "ok", "message": "Graph invocation placeholder"}
