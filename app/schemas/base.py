from pydantic import BaseModel


class BaseResponseDto(BaseModel):
    code: str
    message: str