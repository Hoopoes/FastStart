from pydantic import BaseModel


class BaseResponse(BaseModel):
    resp_code: str
    resp_description: str


# Global response definitions
GLOBAL_RESPONSES = {
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": BaseResponse(resp_code="REQ_VALIDATION_FAILED", resp_description="Field 'name' - This field is required").model_dump()
            }
        },
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": BaseResponse(resp_code="INTERNAL_SERVER_ERROR", resp_description="Internal Server Error").model_dump()
            }
        },
    },
}