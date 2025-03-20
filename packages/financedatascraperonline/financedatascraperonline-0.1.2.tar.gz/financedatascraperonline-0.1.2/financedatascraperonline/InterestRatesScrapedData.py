### Imports

# Tables, math, and graphing
import numpy as np
import pandas as pd

# APIs and scraping
import requests
import lxml

class InterestRatesScrapedData:
    """
    Singleton class (instantiated once) containing methods for scraping public data.
    We want a singleton class with the scraped data as properties because we don't want to re-scrape the same exact data multiple times (i.e. whenever this class is instantiated).
    """
    _instance = None

    # Ensures the class is a singleton, i.e. is only instantiated once.
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._forward_SOFR_curves_df = None
        self._allowed_SOFR_lengths_months = None
        self._treasury_bill_rates_df = None

    def get_scraped_SOFR_curves(self) -> tuple[pd.DataFrame, list]:
        if self._allowed_SOFR_lengths_months is None:
            self._forward_SOFR_curves_df, self._allowed_SOFR_lengths_months = self.__scrape_forward_SOFR_curves()
        return self._forward_SOFR_curves_df, self._allowed_SOFR_lengths_months

    def get_scraped_treasury_bill_rates(self) -> pd.DataFrame:
        if self._treasury_bill_rates_df is None:
            self._treasury_bill_rates_df = self.__scrape_treasury_bill_rates()
        return self._treasury_bill_rates_df

    @staticmethod
    def __scrape_forward_SOFR_curves() -> tuple[pd.DataFrame, list]:
        """
        Scrapes forward 1-month and 3-month SOFR curves for the next 10 years. Indices are the  date of the month when the row values begin applying,
        e.g. if the index is 2025-07-13, then the values for that row apply from that date until the date in the next row, which is ~1 month later.
        NOTE THAT THIS SCRAPING METHOD IS INSECURE AGAINST MALICIOUS WEBSITES.
        """

        # TODO: Store these somewhere safer/nicer than here
        forward_curves_url = "https://www.pensford.com/resources/forward-curve"
        forward_curves_xml = 'https://19621209.fs1.hubspotusercontent-na1.net/hubfs/19621209/FWDCurveTable.xml'

        # Read the data
        response = requests.get(forward_curves_xml)
        tree = lxml.etree.fromstring(response.content)[0][0]
        rows = tree.findall('Row')
        num_rows = len(rows)

        # Create empty dataframe. Would be better to name the columns in a way such that we don't need to hardcode accessing these columns.
        sofr_df = pd.DataFrame(columns=["Date", "1MonthSOFR", "3MonthSOFR"], index=np.arange(num_rows))

        # TODO: See if scraping rows can be vectorized
        for i in range(num_rows):
            row = rows[i]
            date = row.find('ResetDate').text
            one_month_SOFR = row.find('ONEMTSOFR').text.strip("%")
            three_month_SOFR = row.find('THREEMTSOFR').text.strip("%")

            sofr_df.loc[i] = [date, float(one_month_SOFR), float(three_month_SOFR)]

        sofr_df["Date"] = pd.to_datetime(sofr_df["Date"], format="%m/%d/%Y")
        sofr_df = sofr_df.set_index("Date").astype(float)
        allowed_SOFR_lengths = pd.Series(sofr_df.columns).str.split("Month").str.get(0).astype(int).values

        return sofr_df, allowed_SOFR_lengths

    @staticmethod
    def __scrape_treasury_bill_rates() -> pd.DataFrame:
        """
        Here, we scrape the daily treasury bill rates from the US Treasury website for the current year.
        """
        treasury_bill_rates_url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2025/all?field_tdr_date_value=2025&type=daily_treasury_bill_rates&page&_format=csv"
        treasury_bill_rates_df = pd.read_csv(treasury_bill_rates_url)
        return treasury_bill_rates_df