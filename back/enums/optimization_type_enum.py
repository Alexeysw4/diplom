from enum import Enum
from service.optimizers import SharpeOptimizer, MinVolatilityOptimizer
from service.optimizers.base_optimizer import BaseOptimizer


class OptimizationTypeEnum(Enum):
    sharpe = (
        "sharpe",
        SharpeOptimizer,
        "Коэффициент шарпа",
        "Коэффициент шарпа"
    )
    min_volatility = (
        "min_volatility",
        MinVolatilityOptimizer,
        "Минимальная волатильность",
        "Минимальная волатильность"
    )

    def __init__(self, optimization_type: str, optimizer: BaseOptimizer, desc: str, hint: str):
        self.optimization_type = optimization_type
        self.optimizer = optimizer
        self.desc = desc
        self.hint = hint

    @classmethod
    def list(cls):
        return list(map(lambda c: c.optimization_type, cls))

