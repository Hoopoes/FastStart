from fastapi import HTTPException
from app.schemas.base import BaseResponseDto

class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: BaseResponseDto, headers: dict[str, str] | None = None):
        self.detail: BaseResponseDto
        super().__init__(status_code, detail, headers)

############################################
#               Server Errors              #
############################################

class InternalServerError(CustomHTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail=BaseResponseDto(code="INTERNAL_SERVER_ERROR", message="Internal Server Error"))


############################################
#               User Errors                #
############################################

class UserIDAlreadyExist(CustomHTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail=BaseResponseDto(code="USER_ALREADY_EXISTS", message="User ID already exists"))

class UserNameInvalid(CustomHTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail=BaseResponseDto(code="USER_NAME_INVALID", message="Username should not contain special characters"))

class UserNotExist(CustomHTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail=BaseResponseDto(code="USER_NOT_FOUND", message="User not exists with this id"))
        
