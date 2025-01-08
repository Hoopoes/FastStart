from app.utils.logger import LOG
from app.schema.base_schema import BaseResponse
from fastapi import APIRouter, HTTPException, Query
from app.schema.user_schema import CreateUser, UserBase, UserType, Users
from app.res.error import InternalServerError, UserIDAlreadyExist, UserNotExist


tag: str = "User"
user_router: APIRouter = APIRouter(tags=[tag])


@user_router.post('/db/user/create')
async def user_create(req: CreateUser) -> BaseResponse:
    try:

        try:
            LOG.info(f"Create user {req.name}")
        except ValueError:
            raise UserIDAlreadyExist()

        LOG.debug("User created")
        return BaseResponse(resp_code=200, response_description="User Successfully Created")
    
    except HTTPException as ex:
        LOG.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        LOG.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise InternalServerError()


@user_router.delete('/db/user/delete')
async def user_delete(user_id: str = Query(..., max_length=10, description="user id assignment")) -> BaseResponse:
    try:

        user = {
                "name": "umar",
                "user_type": UserType.BUYER
        }
        if user is None:
            raise UserNotExist()
        
        LOG.debug("User deleted")

        return BaseResponse(resp_code=200, response_description="User Successfully Deleted")
    
    except HTTPException as ex:
        LOG.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        LOG.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise InternalServerError()


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

        return Users(resp_code=200, response_description="Success", users=[UserBase.model_validate(user) for user in users])

    except HTTPException as ex:
        LOG.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        LOG.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise InternalServerError()