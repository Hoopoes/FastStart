import app.errors.error as http_error
from app.schemas.base import BaseResponseDto


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