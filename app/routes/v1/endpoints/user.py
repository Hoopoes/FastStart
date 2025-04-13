import re
import uuid
from fastapi import APIRouter, Query


from app.core.logger import LOG
import app.errors.error as http_error
import app.services.user_db as user_db
from app.schemas.base import BaseResponseDto
from app.utils.helpers import handle_exception
from app.core.log_handler import set_log_context
from app.errors.openapi_error import UserResponseDoc
from app.schemas.user import CreateUserDto, UsersDto



user_router = APIRouter()


@user_router.get('/fetch')
async def fetch_users() -> UsersDto:
    try:
        users = await user_db.fetch_all()
        # Attach custom data to the log entry using 'extra'
        LOG.debug("user list", extra={"obj": [_.model_dump() for _ in users]})

        return UsersDto(code="SUCCESS", message="Success", users=users)

    except Exception as ex:
        handle_exception(ex)
    

@user_router.post('/create', responses=UserResponseDoc.create)
async def create_user(req: CreateUserDto) -> BaseResponseDto:

    # Set log context for this API function
    set_log_context(user_id=req.user_id, uuid=str(uuid.uuid4()))

    try:
        
        try:
            if re.search(r"[^a-zA-Z0-9_]", req.name):
                raise http_error.UserNameInvalid()
            await user_db.create(user_id=req.user_id, name=req.name, user_type=req.user_type)
            LOG.info(f"Create user {req.name}")
        except ValueError:
            raise http_error.UserIDAlreadyExist()
        

        LOG.debug("User created")
        return BaseResponseDto(code="SUCCESS", message="User Successfully Created")
    
    except Exception as ex:
        handle_exception(ex)

@user_router.delete('/delete', responses=UserResponseDoc.delete)
async def delete_user(user_id: str = Query(..., max_length=10, description="user id assignment")) -> BaseResponseDto:

    # Set log context for this API function
    set_log_context(user_id=user_id, uuid=str(uuid.uuid4()))

    try:

        user = await user_db.delete(user_id=user_id)

        if user is None:
            raise http_error.UserNotExist()
        
        LOG.debug("User deleted")

        return BaseResponseDto(code="SUCCESS", message="User Successfully Deleted")
    
    except Exception as ex:
        handle_exception(ex)