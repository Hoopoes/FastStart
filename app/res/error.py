from fastapi import HTTPException
from app.schema.base_schema import BaseResponse

############################################
#               Server Errors              #
############################################

class InternalServerError(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail=BaseResponse(code="INTERNAL_SERVER_ERROR", message="Internal Server Error"))


############################################
#               User Errors                #
############################################

class UserIDAlreadyExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail=BaseResponse(code="USER_ALREADY_EXISTS", message="User ID already exists"))

class UserNameInvalid(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail=BaseResponse(code="USER_NAME_INVALID", message="Username should not contain special characters"))

class UserNotExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail=BaseResponse(code="USER_NOT_FOUND", message="User not exists with this id"))
        
