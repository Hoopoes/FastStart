from typing import Literal
from fastapi import status
from fastapi import HTTPException

from app.schemas.base import BaseResponseDto


class CustomHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        headers: dict[str, str] | None = None,
    ):
        self.detail = BaseResponseDto(code=code, message=message)
        super().__init__(status_code, self.detail, headers)


############################################
#               Server Errors              #
############################################


class InternalServerError(CustomHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="INTERNAL_SERVER_ERROR",
            message="Internal Server Error",
        )


############################################
#               Auth Errors              #
############################################


class InvalidAuthentication(CustomHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="INVALID_AUTHENTICATION",
            message="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidCredentials(CustomHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="INVALID_CREDENTIALS",
            message="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidToken(CustomHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="INVALID_TOKEN",
            message="Invalid or malformed authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidTokenType(CustomHTTPException):
    def __init__(self, token_type: Literal["access", "refresh"]):
        required = "Access token" if token_type == "access" else "Refresh token"
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="INVALID_TOKEN_TYPE",
            message=f"Invalid token type. {required} required.",
        )

class TokenExpired(CustomHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="TOKEN_EXPIRED",
            message="Authentication token has expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )

############################################
#               User Errors                #
############################################


class UserIDAlreadyExist(CustomHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="USER_ALREADY_EXISTS",
            message="User ID already exists",
        )


class UserNameInvalid(CustomHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="USER_NAME_INVALID",
            message="Username should not contain special characters",
        )


class UserNotExist(CustomHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="USER_NOT_FOUND",
            message="User not exists with this id",
        )
