from fastapi import HTTPException

import app.errors.error as http_error
from app.schemas.base import BaseResponseDto


def error_example(response: HTTPException):
    detail: BaseResponseDto
    if isinstance(response, HTTPException):
        if isinstance(response.detail, BaseResponseDto):
            detail = response.detail
            return {"summary": type(response).__name__, "value": detail.model_dump()}
    return {"summary": "", "value": {}}


def error_by_status(status_code: int, description: str, *exceptions: HTTPException):
    return (status_code, description, list(exceptions))


def generate_error_docs(errors: list[tuple[int, str, list[HTTPException]]]):
    result = {}
    
    for status_code, description, exceptions in errors:
        # Initialize the base error response
        error_response = {
            "description": description,
            "content": {
                "application/json": {
                    "examples": {
                        type(err).__name__.lower(): error_example(err) 
                        for err in exceptions
                    }
                }
            }
        }

        # Ensure InternalServerError is included for 500 status
        if status_code == 500:
            if not any(isinstance(err, http_error.InternalServerError) for err in exceptions):
                # Add InternalServerError if not present
                err = http_error.InternalServerError()
                error_response["content"]["application/json"]["examples"].setdefault(
                    type(err).__name__.lower(), 
                    error_example(err)
                )

        result[status_code] = error_response

    return result