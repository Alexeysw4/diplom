from fastapi import HTTPException


class NoOptimalPortfolioException(HTTPException):
    def __init__(self,) -> None:
        super().__init__(
            status_code=400,
            detail="Для выбранных данных не получилось составить портфель, который уходит в плюс :("
        )
