from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, detail):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = detail


class ErrorException(HTTPException):
    def __init__(self, detail):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail
