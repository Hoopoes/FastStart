import re
import uuid
from fastapi import APIRouter, Query


from app.utils.logger import LOG
import app.errors.error as http_error
from app.schemas.base import BaseResponseDto
from app.utils.log_handler import set_log_context
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

        return UsersDto(users=users)

    except Exception as ex:
        raise ex
    

@user_router.post('/create')
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
    
    except Exception as ex:
        raise ex

@user_router.delete('/delete')
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
    
    except Exception as ex:
        raise ex