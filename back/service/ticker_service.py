import yfinance as yf
from translate import Translator


class TickerService:
    translator = Translator(to_lang="Russian")

    def __init__(self, tickers):
        self.tickers = tickers

    def group_by_sector(self) -> dict[str, float]:
        sectors = {}
        for ticker_name in self.tickers.keys():
            tick_count = float(self.tickers[ticker_name])
            tick_info = yf.Ticker(ticker_name).info
            sector = self.translator.translate(tick_info.get("sector", "Other"))
            if sector not in sectors:
                sectors[sector] = tick_count
            else:
                sectors[sector] += tick_count
        return sectors
