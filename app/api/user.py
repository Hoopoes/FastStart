import app.db.user_db as user_db
from app.utils.logger import LOG
from app.schema.base_schema import BaseResponse
from fastapi import APIRouter, HTTPException, Query
from app.schema.user_schema import CreateUser, Users, UserBase
from app.res.error import InternalServerError, UserIDAlreadyExist, UserNotExist


tag: str = "User"
user_router: APIRouter = APIRouter(tags=[tag])


@user_router.post('/db/user/create')
async def user_create(req: CreateUser) -> BaseResponse:
    try:

        try:
            await user_db.create(user_id=req.user_id, name=req.name, user_type=req.user_type)
        except ValueError:
            raise UserIDAlreadyExist()

        LOG.debug("User created")
        return BaseResponse(resp_code="SUCCESS", resp_description="User Successfully Created")
    
    except HTTPException as ex:
        LOG.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        LOG.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise InternalServerError()


@user_router.delete('/db/user/delete')
async def user_delete(user_id: str = Query(..., max_length=10, description="user id assignment")) -> BaseResponse:
    try:

        user = await user_db.delete(user_id=user_id)

        if user is None:
            raise UserNotExist()
        
        LOG.debug("User deleted")

        return BaseResponse(resp_code="SUCCESS", resp_description="User Successfully Deleted")
    
    except HTTPException as ex:
        LOG.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        LOG.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise InternalServerError()


@user_router.get('/db/user/fetch')
async def users_fetch() -> Users:
    try:
        users = await user_db.fetch_all()

        return Users(resp_code="SUCCESS", resp_description="Success", users=users)

    except HTTPException as ex:
        LOG.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        LOG.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise InternalServerError()