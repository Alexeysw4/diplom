from pypfopt import EfficientFrontier

from .base_optimizer import BaseOptimizer


class SharpeOptimizer(BaseOptimizer):
    def __init__(self, mu, sigma):
        super().__init__(mu, sigma)

    def get_info(self):
        ef = EfficientFrontier(self.mu, self.sigma,
                               weight_bounds=(0, 1))  # weight bounds in negative allows shorting of stocks
        sharpe_pfolio = ef.max_sharpe()  # May use add objective to ensure minimum zero weighting to individual stocks
        sharpe_pwt = ef.clean_weights()
        return sharpe_pwt, ef
