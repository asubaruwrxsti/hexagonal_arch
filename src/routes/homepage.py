from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from adapters.incoming.dependencies import get_db
from core.domain.response import APIResponse

router = APIRouter()

@router.get("/")
async def home():
    return APIResponse(
        status="success",
        message="Welcome to the homepage",
        status_code=200
    )

@router.get("/items/")
async def read_items(db: Session = Depends(get_db)):
    return APIResponse(
        status="success",
        message="Items retrieved successfully",
        status_code=200
    )