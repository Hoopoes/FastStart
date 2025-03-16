import re
from app.utils.logger import LOG
from app.schema.base_schema import BaseResponse
from fastapi import APIRouter, HTTPException, Query
from app.schema.user_schema import CreateUser, UserBase, UserType, Users
from app.res.error_doc import (
    USER_CREATE_RESPONSES, 
    USER_DELETE_RESPONSES
)
from app.res.error import (
    InternalServerError, 
    UserIDAlreadyExist, 
    UserNameInvalid, 
    UserNotExist
)


tag: str = "User"
user_router: APIRouter = APIRouter(tags=[tag])


@user_router.get('/db/user/fetch')
async def users_fetch() -> Users:
    try:
        users = [
            {
                "name": "umar",
                "user_type": UserType.BUYER
            },
            {
                "name": "mubbashir",
                "user_type": UserType.SELLER
            }
        ]

        return Users(code="SUCCESS", message="Success", users=[UserBase.model_validate(user) for user in users])

    except HTTPException as ex:
        LOG.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        LOG.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise InternalServerError()
    

@user_router.post('/db/user/create', responses=USER_CREATE_RESPONSES)
async def user_create(req: CreateUser) -> BaseResponse:
    try:

        try:
            LOG.info(f"Create user {req.name}")
            if re.search(r"[^a-zA-Z0-9_]", req.name):
                raise UserNameInvalid()
        except ValueError:
            raise UserIDAlreadyExist()
        

        LOG.debug("User created")
        return BaseResponse(code="SUCCESS", message="User Successfully Created")
    
    except HTTPException as ex:
        LOG.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        LOG.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise InternalServerError()


@user_router.delete('/db/user/delete', responses=USER_DELETE_RESPONSES)
async def user_delete(user_id: str = Query(..., max_length=10, description="user id assignment")) -> BaseResponse:
    try:

        user = {
                "name": "umar",
                "user_type": UserType.BUYER
        }
        if user is None:
            raise UserNotExist()
        
        LOG.debug("User deleted")

        return BaseResponse(code="SUCCESS", message="User Successfully Deleted")
    
    except HTTPException as ex:
        LOG.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        LOG.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise InternalServerError()