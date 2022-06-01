from fastapi import HTTPException


class SomethingWentWrongException(HTTPException):
    def __init__(self,) -> None:
        super().__init__(
            status_code=400,
            detail="Что-то пошло не так :("
        )
