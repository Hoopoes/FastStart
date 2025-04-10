import re
import uuid
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Query


from app.core.logger import LOG
import app.errors.error as http_error
from app.schemas.base import BaseResponseDto
from app.core.log_handler import set_log_context
from app.errors.openapi_error import UserResponseDoc
from app.schemas.user import CreateUserDto, UsersDto


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
        # Attach custom data to the log entry using 'extra'
        LOG.debug("user list", extra={"obj": users})

        return UsersDto(code="SUCCESS", message="Success", users=users)

    except HTTPException as ex:
        LOG.error("HTTP Exception", extra={
            "obj": ex.detail.model_dump() if isinstance(ex.detail, BaseModel) else ex.detail
        })
        raise ex
    except Exception as ex:
        LOG.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise http_error.InternalServerError()
    

@user_router.post('/create', responses=UserResponseDoc.create)
async def create_user(req: CreateUserDto) -> BaseResponseDto:

    # Set log context for this API function
    set_log_context(user_id=req.user_id, uuid=str(uuid.uuid4()))

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
        LOG.error("HTTP Exception", extra={
            "obj": ex.detail.model_dump() if isinstance(ex.detail, BaseModel) else ex.detail
        })
        raise ex
    except Exception as ex:
        LOG.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise http_error.InternalServerError()

@user_router.delete('/delete', responses=UserResponseDoc.delete)
async def delete_user(user_id: str = Query(..., max_length=10, description="user id assignment")) -> BaseResponseDto:

    # Set log context for this API function
    set_log_context(user_id=user_id, uuid=str(uuid.uuid4()))

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
        LOG.error("HTTP Exception", extra={
            "obj": ex.detail.model_dump() if isinstance(ex.detail, BaseModel) else ex.detail
        })
        raise ex
    except Exception as ex:
        LOG.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise http_error.InternalServerError()