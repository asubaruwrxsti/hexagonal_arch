from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_homepage():
    return {"message": "Welcome to the homepage"}