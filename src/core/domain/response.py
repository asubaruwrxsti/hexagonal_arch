from pydantic import BaseModel
from typing import Any, Optional
from http import HTTPStatus

class APIResponse(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None
    status_code: int = HTTPStatus.OK

    @classmethod
    def error(cls, message: str, status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR) -> 'APIResponse':
        return cls(
            status="error",
            message=message,
            status_code=status_code
        )

    @classmethod
    def success(cls, data: Any = None, message: str = "Success") -> 'APIResponse':
        return cls(
            status="success",
            message=message,
            data=data
        )