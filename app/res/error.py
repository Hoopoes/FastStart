from fastapi import HTTPException
from app.schema.base_schema import BaseResponse

############################################
#               Server Errors              #
############################################

class InternalServerError(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail=BaseResponse(resp_code="INTERNAL_SERVER_ERROR", resp_description="Internal Server Error"))


############################################
#               User Errors                #
############################################

class UserIDAlreadyExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail=BaseResponse(resp_code="USER_ALREADY_EXISTS", resp_description="User ID already exists"))

class UserNotExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail=BaseResponse(resp_code="USER_NOT_FOUND", resp_description="User not exists with this id"))
        
