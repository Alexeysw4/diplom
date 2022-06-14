from .base_exception import BaseHTTPException


class SomethingWentWrongException(BaseHTTPException):
    detail_ = "Что-то пошло не так :("
