from .base_exception import BaseHTTPException


class PredictionNegativeStocksException(BaseHTTPException):
    detail_ = "Модель спрогнозировала отрицательные цены на акции:("
