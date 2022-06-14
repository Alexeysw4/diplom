from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    detail_ = "Ошибка :("

    def __init__(self, data: dict = None) -> None:
        if data is None:
            data = {}
        data['error'] = self.detail_
        super().__init__(
            status_code=400,
            detail=data
        )
