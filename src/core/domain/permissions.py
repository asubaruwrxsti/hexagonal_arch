from enum import Enum
from typing import List
from functools import wraps
from core.domain.response import APIResponse

class Permission(Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"

def require_permissions(required_permissions: List[Permission]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # TODO: Add authentication logic here
            has_permission = True
            
            if not has_permission:
                return APIResponse.error(
                    "Insufficient permissions", 
                    status_code=403
                ).to_response()
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator