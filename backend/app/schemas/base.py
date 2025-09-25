from pydantic import BaseModel
from typing import Optional, Any


class BaseResponse(BaseModel):
    success: bool = True
    message: str = "Success"
    data: Optional[Any] = None