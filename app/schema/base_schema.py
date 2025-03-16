from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: str
    message: str


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
                "example": BaseResponse(code="INTERNAL_SERVER_ERROR", message="Internal Server Error").model_dump()
            }
        },
    },
}