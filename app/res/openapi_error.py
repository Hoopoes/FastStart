from fastapi import HTTPException
from app.schema.base_schema import BaseResponse
from app.res.error import InternalServerError, UserIDAlreadyExist, UserNameInvalid, UserNotExist


def error_example(response: HTTPException):
    detail: BaseResponse
    if isinstance(response, HTTPException):
        if isinstance(response.detail, BaseResponse):
            detail = response.detail
            return {"summary": type(response).__name__, "value": detail.model_dump()}
    return {"summary": "", "value": {}}
    

def error_docs(status_code: int, description: str, exec: list[HTTPException]):
    return {
        status_code: {
            "description": description,
            "content": {
                "application/json": {
                    "examples": {
                        type(value).__name__.lower(): error_example(value) for value in exec
                    }
                }
            }
        }
    }

# Global response definitions
GLOBAL_RESPONSES = {
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": BaseResponse(code="REQ_VALIDATION_FAILED", message="Field 'name' - This field is required").model_dump()
            }
        },
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": InternalServerError().detail.model_dump()
            }
        },
    },
}


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