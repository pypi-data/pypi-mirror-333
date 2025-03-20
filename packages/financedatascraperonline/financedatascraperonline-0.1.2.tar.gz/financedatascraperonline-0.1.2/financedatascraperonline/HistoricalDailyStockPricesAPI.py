### Imports

# Tables, math, and graphing
import numpy as np
import pandas as pd

# APIs and scraping
from yfinance import Ticker

"""
This class focuses on scraping historical daily stock prices from Yahoo Finance,
and then calculating the most commonly asked for values from historical data:
annualized avg daily return mu, annualized volatility of returns sigma, and latest closing stock price.
"""
class HistoricalDailyStockPricesAPI:
    # We create a singleton class so there's no chance of us recalculating things we've already calculated
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HistoricalDailyStockPricesAPI, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        # Setting constants which will be used throughout
        self.trading_days_per_year = 252
        self.trading_days_per_month = 21

        self.daily_returns = dict()

    def get_historical_prices_df(self, ticker_symbol: str) -> pd.DataFrame:
        """
        Public method for getting historical prices using the yahoofinance library. If a stock has already been scraped, we do not scrape it again. Otherwise, we do scrape for the specified stock.
        This ensures not scraping multiple times, which is unneeded and unhelpful.
        """

        if ticker_symbol not in self.daily_returns.keys():
            try:
                self.daily_returns[ticker_symbol] = self.__scrape_historical_prices(ticker_symbol, self.trading_days_per_year)
            except:
                raise ValueError(f"The stock {ticker_symbol} is not present in yahoofinance. Please use the 3 or 4 letter stock abbreviation for a stock in yahoofinance, e.g. AAPL.")

        return self.daily_returns[ticker_symbol]

    def get_main_stats_from_hist_prices(self, ticker_symbol: str) -> tuple[float, float, float]:
        """
        Public method for getting the most commonly asked for values from historical data: annualized avg daily return mu, annualized volatility of returns sigma, and latest closing stock price.
        """
        return self.__get_main_stats_from_hist_prices(self.get_historical_prices_df(ticker_symbol), self.trading_days_per_year)

    @staticmethod
    def __get_main_stats_from_hist_prices(historical_data: pd.DataFrame, trading_days_per_year: int = 252) -> tuple[float, float, float]:
        """
        Helper method for getting the most commonly asked for values from historical data: annualized avg daily return mu, annualized volatility of returns sigma, and latest price.
        """
        mu = historical_data["Annualized_Mean_Daily_Return"].iloc[-1]
        sigma = historical_data["Annualized_Hist_Volatility"].iloc[-1]
        latest_price = historical_data["Close"].iloc[-1]

        return mu, sigma, latest_price

    @staticmethod
    def __scrape_historical_prices(ticker_symbol: str, trading_days_per_year: int = 252) -> pd.DataFrame:
        """
        Private method for getting historical prices using the yahoofinance library.
        We automatically only scrape the last 3 years of data for any stock, since more time than that may potentially be irrelevant.
        It is acknowledged that this is a somewhat arbitrary choice, and in reality, the amount of time that it may make sense to scrape may vary depending on historical circumstances and the stock.
        For instance, I wouldn't want to include COVID era whatsoever.

        param ticker_symbol: The stock name, e.g. AAPL
        return historical_data: A dataframe with the following columns: [Close, Log_Close, Daily_Returns, Annualized_Hist_Volatility, Annualized_Mean_Daily_Return] with a daily datetime index.
        Includes the values for the past 3 years for the specified stock.
        """
        # Create a Ticker object
        ticker = Ticker(ticker_symbol)

        # Fetch historical market data
        historical_data = ticker.history(period="3y")
        historical_data = historical_data[['Close']]

        # Here, we find the log daily returns and take the moving volatility using a 1-year rolling window (again, an arbitrary choice).
        historical_data["Log_Close"] = np.log(historical_data["Close"])
        historical_data['Daily_Returns'] = historical_data['Log_Close'].diff()
        historical_data['Annualized_Hist_Volatility'] = historical_data['Daily_Returns'].rolling(trading_days_per_year).std() * np.sqrt(trading_days_per_year)
        historical_data['Annualized_Mean_Daily_Return'] = historical_data['Daily_Returns'].rolling(trading_days_per_year).mean() * trading_days_per_year

        # TODO: See if we can get implied volatility from historical option prices as well

        historical_data.index = pd.to_datetime(historical_data.index.date)
        return historical_data