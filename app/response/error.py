from fastapi import HTTPException

class UserIDAlreadyExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User ID already exists")

class UserNotExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User not exists with this id")
        
class DatabaseUnreachable(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail="Database unreachable")