import re
from app.core.logger import LOG
import app.res.error as http_error
from app.schema.base import BaseResponseDto
from app.res.openapi_error import UserResponseDoc
from fastapi import APIRouter, HTTPException, Query
from app.schema.user import CreateUserDto, UsersDto


user_router = APIRouter()


@user_router.get('/fetch')
async def fetch_users() -> UsersDto:
    try:
        users = [
            {
                "user_id": "2121",
                "name": "umar",
                "user_type": "BUYER"
            },
            {
                "user_id": "2123",
                "name": "mubbashir",
                "user_type": "SELLER"
            }
        ]
        LOG.debug("user list", extra={"user list": users})

        return UsersDto(code="SUCCESS", message="Success", users=users)

    except HTTPException as ex:
        LOG.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        LOG.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise http_error.InternalServerError()
    

@user_router.post('/create', responses=UserResponseDoc.create)
async def create_user(req: CreateUserDto) -> BaseResponseDto:
    try:

        try:
            if re.search(r"[^a-zA-Z0-9_]", req.name):
                raise http_error.UserNameInvalid()
            LOG.info(f"Create user {req.name}")
        except ValueError:
            raise http_error.UserIDAlreadyExist()
        

        LOG.debug("User created")
        return BaseResponseDto(code="SUCCESS", message="User Successfully Created")
    
    except HTTPException as ex:
        LOG.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        LOG.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise http_error.InternalServerError()


@user_router.delete('/delete', responses=UserResponseDoc.delete)
async def delete_user(user_id: str = Query(..., max_length=10, description="user id assignment")) -> BaseResponseDto:
    try:

        user = {
            "name": "umar",
            "user_type": "BUYER"
        }
        if user is None:
            raise http_error.UserNotExist()
        
        LOG.debug("User deleted")

        return BaseResponseDto(code="SUCCESS", message="User Successfully Deleted")
    
    except HTTPException as ex:
        LOG.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        LOG.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise http_error.InternalServerError()