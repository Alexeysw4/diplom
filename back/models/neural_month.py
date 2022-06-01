import math

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler

from .base_model import BaseModel


class NeuralMonth(BaseModel):
    def __init__(self, data, month):
        super().__init__(data, month)

    @staticmethod
    def get_predictions_by_column(data, month):
        dataset = data.values
        training_data_len = math.ceil(len(dataset) * .8)

        window_length = 20

        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset.reshape(-1, 1))

        train_data = scaled_data[0:training_data_len]
        x_train = []
        y_train = []

        for i in range(window_length, len(train_data)):
            x_train.append(train_data[i - window_length:i])
            y_train.append(train_data[i])

        x_train, y_train = np.array(x_train), np.array(y_train)

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], x_train.shape[2]))

        model = Sequential()
        model.add(LSTM(window_length, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
        model.add(Dropout(0.2))
        model.add(LSTM(window_length, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(1, activation='linear'))

        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

        model.fit(x_train, y_train, batch_size=3, epochs=6)

        scaled = scaled_data.copy()

        days = []
        for i in range(len(data), len(data) + month):
            days.append(i)

        res = []
        for i in range(0, len(days)):
            test_data = scaled[len(scaled) - window_length:]
            x_test = []
            for i in range(window_length, len(test_data) + 1):
                x_test.append(test_data[i - window_length:i])
            x_test = np.array(x_test)
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], x_test.shape[2]))
            predictions = model.predict(x_test)
            ar = list(scaled)
            ar.append(predictions[0])
            scaled = np.array(ar)
            predictions = scaler.inverse_transform(predictions)
            res.append(predictions[0][0])

        return res
