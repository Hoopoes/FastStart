import app.errors.error as http_error
from app.schemas.base import BaseResponseDto
from app.errors.openapi_errors import error_by_status, generate_error_docs


# Global response definitions
GLOBAL_RESPONSES = {
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": BaseResponseDto(code="REQ_VALIDATION_FAILED", message="Field 'name' - This field is required").model_dump()
            }
        },
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": http_error.InternalServerError().detail.model_dump()
            }
        },
    },
}



class UserResponseDoc:

    create = generate_error_docs([
        error_by_status(400, "Bad Request", 
            http_error.UserIDAlreadyExist(), 
            http_error.UserNameInvalid()
        ),
    ])
    
    delete = generate_error_docs([
        error_by_status(400, "Bad Request",
            http_error.UserNotExist(),
        ),
    ])