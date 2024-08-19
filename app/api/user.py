from app.utils.logger import log
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Query
from app.schema.user_schema import CreateUser, UserBase, UserType
from app.response.error import UserIDAlreadyExist, UserNotExist


tag: str = "User"
user_router: APIRouter = APIRouter(tags=[tag])


@user_router.post('/api/db/user/create')
async def user_create(req: CreateUser = Depends()) -> JSONResponse:

    try:
        log.info(f"Create user {req.name}")
    except ValueError:
        raise UserIDAlreadyExist()

    log.debug("User created")
    return JSONResponse(content={"response": "User Successfully Created"}, status_code=200)


@user_router.delete('/api/db/user/delete')
async def user_delete(user_id: str = Query(..., max_length=10, description="user id assignment")) -> JSONResponse:

    user = {
            "name": "umar",
            "user_type": UserType.BUYER
    }
    if user is None:
        raise UserNotExist()
    
    log.debug("User deleted")
    return JSONResponse(content={"response": "User Successfully Deleted"}, status_code=200)


@user_router.get('/api/db/user/fetch', response_model=list[UserBase])
async def users_fetch() -> list[UserBase]:
    
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

    return [UserBase.model_validate(user) for user in users]