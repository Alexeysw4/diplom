import yfinance as yf


class DataService:
    def __init__(self, tickers_name, start, end, interval):
        self.tickers = tickers_name.split(",")
        self.start = start
        self.end = end
        self.interval = interval

    def get_data(self):
        return yf.download(self.tickers, start=self.start, end=self.end, interval=self.interval)['Adj Close']
