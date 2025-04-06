import re
from fastapi import APIRouter, HTTPException, Query

import app.db.user_db as user_db
import app.errors.error as http_error
from app.core.logger import get_logger
from app.schemas.base import BaseResponseDto
from app.errors.openapi_error import UserResponseDoc
from app.schemas.user import CreateUserDto, UsersDto


user_router = APIRouter()


@user_router.get('/fetch')
async def fetch_users() -> UsersDto:
    logger = get_logger()
    try:
        users = await user_db.fetch_all()
        logger.debug("user list", extra={"obj": [_.model_dump() for _ in users]})

        return UsersDto(code="SUCCESS", message="Success", users=users)
    
    except HTTPException as ex:
        logger.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        logger.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise http_error.InternalServerError()
    

@user_router.post('/create', responses=UserResponseDoc.create)
async def create_user(req: CreateUserDto) -> BaseResponseDto:
    logger = get_logger(user_id=req.user_id)
    try:
        
        try:
            if re.search(r"[^a-zA-Z0-9_]", req.name):
                raise http_error.UserNameInvalid()
            await user_db.create(user_id=req.user_id, name=req.name, user_type=req.user_type)
            logger.info(f"Create user {req.name}")
        except ValueError:
            raise http_error.UserIDAlreadyExist()
        

        logger.debug("User created")
        return BaseResponseDto(code="SUCCESS", message="User Successfully Created")
    
    except HTTPException as ex:
        logger.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        logger.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise http_error.InternalServerError()


@user_router.delete('/delete', responses=UserResponseDoc.delete)
async def delete_user(user_id: str = Query(..., max_length=10, description="user id assignment")) -> BaseResponseDto:
    logger = get_logger(user_id=user_id)
    try:

        user = await user_db.delete(user_id=user_id)

        if user is None:
            raise http_error.UserNotExist()
        
        logger.debug("User deleted")

        return BaseResponseDto(code="SUCCESS", message="User Successfully Deleted")
    

    except HTTPException as ex:
        logger.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        logger.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise http_error.InternalServerError()