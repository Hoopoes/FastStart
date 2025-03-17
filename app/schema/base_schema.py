from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: str
    message: str