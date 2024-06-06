import app.db.user_db as user_db
from app.utils.logger import log
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Query
from app.schemas.user_schema import CreateUser, UserBase
from app.responses.error import UserIDAlreadyExist, UserNotExist


tag: str = "User"
user_router: APIRouter = APIRouter(tags=[tag])


@user_router.post('/api/db/user/create')
async def user_create(req: CreateUser = Depends()) -> JSONResponse:

    try:
        await user_db.create(user_id=req.user_id, name=req.name, user_type=req.user_type)
    except ValueError:
        raise UserIDAlreadyExist()

    log.debug("User created")
    return JSONResponse(content={"response": "User Successfully Created"}, status_code=200)


@user_router.delete('/api/db/user/delete')
async def user_delete(user_id: str = Query(..., max_length=10, description="user id assignment")) -> JSONResponse:

    user = await user_db.delete(user_id=user_id)
    if user is None:
        raise UserNotExist()
    
    log.debug("User deleted")
    return JSONResponse(content={"response": "User Successfully Deleted"}, status_code=200)


@user_router.get('/api/db/user/fetch', response_model=list[UserBase])
async def users_fetch() -> list[UserBase]:
    
    users = await user_db.fetch_all()

    return [UserBase.model_validate(user.model_dump()) for user in users]