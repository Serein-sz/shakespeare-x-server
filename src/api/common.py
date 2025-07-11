from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None
    errors: Optional[List[str]] = None
    
    @classmethod
    def success(cls, message: str, data: Optional[T] = None):
        return cls(code=200, message=message, data=data)

    @classmethod
    def fail(cls, message: str, data: Optional[T] = None):
        return cls(code=500, message=message, data=data)
