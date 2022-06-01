from abc import ABCMeta, abstractmethod


class BaseOptimizer(metaclass=ABCMeta):
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    @abstractmethod
    def get_info(self):
        """:return (pwt, ef)"""
        pass