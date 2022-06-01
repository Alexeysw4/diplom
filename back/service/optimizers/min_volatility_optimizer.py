from pypfopt import EfficientFrontier

from .base_optimizer import BaseOptimizer


class MinVolatilityOptimizer(BaseOptimizer):
    def __init__(self, mu, sigma):
        super().__init__(mu, sigma)

    def get_info(self):
        ef = EfficientFrontier(self.mu, self.sigma,
                               weight_bounds=(0, 1))
        minvol = ef.min_volatility()
        minvol_pwt = ef.clean_weights()
        return minvol_pwt, ef
