from app.utils.logger import log
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schema.base_schema import BaseResponse
from app.res.error import InternalServerError, UserIDAlreadyExist, UserNotExist
from app.schema.user_schema import CreateUser, UserBase, UserType, Users



tag: str = "User"
user_router: APIRouter = APIRouter(tags=[tag])


@user_router.post('/api/db/user/create')
async def user_create(req: CreateUser = Depends()) -> BaseResponse:
    try:

        try:
            log.info(f"Create user {req.name}")
        except ValueError:
            raise UserIDAlreadyExist()

        log.debug("User created")
        return BaseResponse(resp_code=200, response="User Successfully Created")
    
    except HTTPException as ex:
        log.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        log.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise InternalServerError()


@user_router.delete('/api/db/user/delete')
async def user_delete(user_id: str = Query(..., max_length=10, description="user id assignment")) -> BaseResponse:
    try:

        user = {
                "name": "umar",
                "user_type": UserType.BUYER
        }
        if user is None:
            raise UserNotExist()
        
        log.debug("User deleted")

        return BaseResponse(resp_code=200, response="User Successfully Deleted")
    
    except HTTPException as ex:
        log.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        log.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise InternalServerError()


@user_router.get('/api/db/user/fetch')
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

        return Users(resp_code=200, response="Success", users=[UserBase.model_validate(user) for user in users])

    except HTTPException as ex:
        log.error(f"HTTP Exception: {ex.detail}")
        raise ex
    except Exception as ex:
        log.error(f"Unexpected error occurred: {ex}", exc_info=True)
        raise InternalServerError()