from pydantic import BaseModel
from fastapi import HTTPException


from app.core.logger import LOG
import app.errors.error as http_error


# Helper function to handle exceptions and log errors
def handle_exception(ex: Exception):
    if isinstance(ex, HTTPException):
        LOG.error("HTTP Exception", extra={
            "obj": ex.detail.model_dump() if isinstance(ex.detail, BaseModel) else ex.detail
        })
        raise ex
    else:
        LOG.error(f"Unexpected error occurred: {ex}", exc_info=True)
    raise http_error.InternalServerError()  # General server error response