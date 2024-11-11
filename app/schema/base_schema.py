from pydantic import BaseModel


class BaseResponse(BaseModel):
    resp_code: int
    response: str