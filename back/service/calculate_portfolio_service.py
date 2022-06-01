from pypfopt import expected_returns, risk_models, get_latest_prices, DiscreteAllocation


class CalculatePortfolioService:
    def __init__(self, data, optimization_type):
        self.data = data
        self.optimization_type = optimization_type

    def calculate(self, total_sum: int) -> tuple:
        # Годовая доходность
        mu = expected_returns.mean_historical_return(self.data)
        # Дисперсия портфеля
        Sigma = risk_models.sample_cov(self.data)

        pwt, ef = self.optimization_type.optimizer(mu, Sigma).get_info()

        latest_prices1 = get_latest_prices(self.data)
        allocation_shp, rem_shp = DiscreteAllocation(pwt, latest_prices1,
                                                     total_portfolio_value=total_sum).lp_portfolio()
        return allocation_shp, rem_shp, ef.portfolio_performance(verbose=True)
