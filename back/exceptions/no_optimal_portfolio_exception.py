from .base_exception import BaseHTTPException


class NoOptimalPortfolioException(BaseHTTPException):
    detail_ = "Для выбранных данных не получилось составить портфель, который уходит в плюс :("
