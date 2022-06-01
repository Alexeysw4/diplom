from fastapi import HTTPException


class PredictionNegativeStocksException(HTTPException):
    def __init__(self,) -> None:
        super().__init__(
            status_code=400,
            detail="Модель спрогнозировала отрицательные цены на акции:("
        )
