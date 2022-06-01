from abc import ABCMeta, abstractmethod

import pandas as pd


class BaseModel(metaclass=ABCMeta):

    def __init__(self, data, month):
        self.data = data
        self.month = month

    @staticmethod
    @abstractmethod
    def get_predictions_by_column(data, month):
        pass

    def get_table_of_predictions(self) -> pd.DataFrame:
        d_of_values = {}
        count = len(self.data.columns.tolist())

        for i in range(0, count):
            res = self.get_predictions_by_column(self.data.iloc[:, i], self.month)
            d_of_values[self.data.columns.tolist()[i]] = res

        df = pd.DataFrame(d_of_values)

        return df
