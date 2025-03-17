import re
import app.db.user_db as user_db
from app.utils.logger import LOG
from app.schema.base_schema import BaseResponse
from fastapi import APIRouter, HTTPException, Query
from app.schema.user_schema import CreateUser, Users
from app.res.openapi_error import (
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
async def fetch_users() -> Users:
    try:
        users = await user_db.fetch_all()

        return Users(code="SUCCESS", message="Success", users=users)
    
    except HTTPException as ex:
        LOG.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        LOG.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise InternalServerError()


@user_router.post('/db/user/create', responses=USER_CREATE_RESPONSES)
async def create_user(req: CreateUser) -> BaseResponse:
    try:

        try:
            if re.search(r"[^a-zA-Z0-9_]", req.name):
                raise UserNameInvalid()
            await user_db.create(user_id=req.user_id, name=req.name, user_type=req.user_type)
            LOG.info(f"Create user {req.name}")
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
async def delete_user(user_id: str = Query(..., max_length=10, description="user id assignment")) -> BaseResponse:
    try:

        user = await user_db.delete(user_id=user_id)

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