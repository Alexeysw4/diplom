import math

from statsmodels.tsa.statespace.sarimax import SARIMAX

from .base_model import BaseModel


class Arima(BaseModel):
    def __init__(self, data, month):
        super().__init__(data, month)

    @staticmethod
    def get_predictions_by_column(data, month):
        training_data_len = math.ceil(len(data) * .8)
        train = data[0:training_data_len]

        model = SARIMAX(train,
                        order=(0, 1, 0),
                        seasonal_order=(0, 1, 0, 12))
        result = model.fit()

        start = len(data)
        end = (len(data) - 1) + month
        forecast = result.predict(start, end)

        return forecast
