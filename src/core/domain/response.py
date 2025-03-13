from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
from http import HTTPStatus
from fastapi.responses import JSONResponse

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    status: str
    message: str
    data: Optional[T] = None
    status_code: int = HTTPStatus.OK

    @classmethod
    def error(cls, message: str, status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR) -> 'APIResponse[None]':
        return cls(
            status="error",
            message=message,
            status_code=status_code
        )

    @classmethod
    def success(cls, data: T = None, message: str = "Success") -> 'APIResponse[T]':
        return cls(
            status="success",
            message=message,
            data=data,
        )
    
    def to_response(self) -> JSONResponse:
        """Convert this APIResponse to a FastAPI JSONResponse object."""
        return JSONResponse(
            content=self.model_dump(exclude={"status_code"}),
            status_code=self.status_code
        )