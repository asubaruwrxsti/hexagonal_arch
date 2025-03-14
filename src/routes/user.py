from fastapi import APIRouter, Depends
from http import HTTPStatus
from sqlalchemy.orm import Session

from core.domain.response import APIResponse
from core.domain.schemas import UserResponse, UserCreate
from adapters.incoming.dependencies import get_db
from adapters.repositories.user_repository import UserRepository
from core.domain.permissions import Permission, require_permissions

router = APIRouter()

@router.get("/users/{user_id}", response_model=APIResponse[UserResponse])
@require_permissions([Permission.READ])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_repo = UserRepository(session=db)
    user = user_repo.get_by_id(user_id)
    if not user:
        return APIResponse.error("User not found", HTTPStatus.NOT_FOUND).to_response()
    return APIResponse.success(data=user).to_response()

@router.get("/users/")
@require_permissions([Permission.READ])
async def read_users(db: Session = Depends(get_db)):
    try:
        user_repo = UserRepository(session=db)
        users = user_repo.get_all()
        user_responses = [UserResponse.model_validate(user) for user in users]
        return APIResponse.success(user_responses).to_response()
    except Exception as e:
        return APIResponse.error(str(e)).to_response()

@router.post("/users/", status_code=HTTPStatus.CREATED)
@require_permissions([Permission.CREATE])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_repo = UserRepository(session=db)
    
    success, result = user_repo.create_with_email_check(user)
    if not success:
        return APIResponse.error(message=result, status_code=HTTPStatus.CONFLICT).to_response()
    
    user_response = UserResponse.model_validate(result)
    return APIResponse.success(data=user_response, message="User created successfully").to_response()