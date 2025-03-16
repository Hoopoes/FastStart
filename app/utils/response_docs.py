from fastapi import HTTPException
from app.schema.base_schema import BaseResponse
    
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