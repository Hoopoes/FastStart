from app.utils.response_docs import error_docs
from app.res.error import UserIDAlreadyExist, UserNameInvalid, UserNotExist


# User APIs

USER_CREATE_RESPONSES = error_docs(status_code=400, description="User Create Errors",
    exec=[
        UserIDAlreadyExist(),
        UserNameInvalid()
    ]
)
USER_DELETE_RESPONSES = error_docs(status_code=400, description="User Delete Errors",
    exec=[
        UserNotExist()
    ]
)