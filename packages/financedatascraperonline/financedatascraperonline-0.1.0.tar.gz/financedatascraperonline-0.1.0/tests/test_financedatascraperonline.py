from financedatascraperonline import FinanceOnlineDataScraper, InterestRatesScrapedData
import unittest
import pandas as pd
import numpy as np

class test_InterestRatesScrapedData(unittest.TestCase):
    def test_get_scraped_SOFR_curves(self):
        # Arrange
        irsd = InterestRatesScrapedData()
        # Act
        forward_SOFR_curves_df, allowed_SOFR_lengths_months = irsd.get_scraped_SOFR_curves()
        # Assert
        self.assertTrue(isinstance(forward_SOFR_curves_df, pd.DataFrame))
        self.assertTrue(isinstance(allowed_SOFR_lengths_months, np.ndarray))

        # TODO: Check actual format of the dataframe

    def test_get_scraped_treasury_bill_rates(self):
        # Arrange
        irsd = InterestRatesScrapedData()
        # Act
        treasury_bill_rates_df = irsd.get_scraped_treasury_bill_rates()
        # Assert
        self.assertTrue(isinstance(treasury_bill_rates_df, pd.DataFrame))

        # TODO: Check actual format of the dataframe

class test_FinanceOnlineDataScraper(unittest.TestCase):
    def test_get_historical_prices_df(self):
        # Arrange
        fod = FinanceOnlineDataScraper()
        # Act
        aapl_df = fod.get_historical_prices_df("AAPL")
        # Assert
        self.assertTrue(isinstance(aapl_df, pd.DataFrame))
        
        # TODO: Check actual format of the dataframe

    def test_get_main_stats_from_hist_prices(self):
        # Arrange
        fod = FinanceOnlineDataScraper()
        # Act
        mu, sigma, latest_price = fod.get_main_stats_from_hist_prices("AAPL")
        # Assert
        self.assertTrue(isinstance(mu, float))
        self.assertTrue(isinstance(sigma, float))
        self.assertTrue(isinstance(latest_price, float))

        # TODO: Check format and values of the returned values

if __name__ == '__main__':
    unittest.main()