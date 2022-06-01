from enum import Enum
from models import Arima, NeuralMonth
from models.base_model import BaseModel


class ModelMappingEnum(Enum):
    arima = (
        "arima",
        Arima,
        "1mo",
        True,
        "Модель предсказания ARIMA",
        "Временные ряды по месяцам"
    )
    neural_month = (
        "neural_month",
        NeuralMonth,
        "1mo",
        True,
        "Нейронная сеть",
        "Нейронная сеть по месяцам"
    )

    def __init__(self, model_name: str, model: BaseModel, interval: str, need_drop: bool, desc: str, hint: str):
        self.model_name = model_name
        self.model = model
        self.interval = interval
        self.need_drop = need_drop
        self.desc = desc
        self.hint = hint

    @classmethod
    def list(cls):
        return list(map(lambda c: c.model_name, cls))
