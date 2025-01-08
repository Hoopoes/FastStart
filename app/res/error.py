from fastapi import HTTPException
from app.schema.base_schema import BaseResponse

class InternalServerError(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail=BaseResponse(resp_code=500, response_description="Internal Server Error"))

class UserIDAlreadyExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail=BaseResponse(resp_code=400, response_description="User ID already exists"))

class UserNotExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail=BaseResponse(resp_code=400, response_description="User not exists with this id"))
        
