import re

import app.errors.error as http_error

NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_ ]+$")  # letters, digits, _ and spaces


def _validate_name(name: str | None) -> None:
    if name is not None and not NAME_PATTERN.match(name):
        raise http_error.UserNameInvalid()