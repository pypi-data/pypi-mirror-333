import datetime
import logging
import multiprocessing
import sys

import limexhub
import pandas as pd
from click import progressbar
from exchange_calendars import ExchangeCalendar
from joblib import Parallel, delayed
from lime_trader.models.market import Period

from ziplime.data.abstract_historical_market_data_provider import AbstractHistoricalMarketDataProvider


def fetch_historical_limex_data_task(date_from: datetime.datetime,
                                     date_to: datetime.datetime,
                                     exchange_calendar: ExchangeCalendar,
                                     limex_api_key: str, symbol: str, period: Period):
    limex_client = limexhub.RestAPI(token=limex_api_key)
    timeframe = 3
    if period == Period.MINUTE:
        timeframe = 1
    elif period == Period.HOUR:
        timeframe = 2
    elif period == Period.DAY:
        timeframe = 3
    elif period == Period.WEEK:
        timeframe = 4
    elif period == Period.MONTH:
        timeframe = 5
    elif period == Period.QUARTER:
        timeframe = 6
    df = limex_client.candles(symbol=symbol,
                              from_date=date_from.strftime("%Y-%m-%d"),
                              to_date=date_to.strftime("%Y-%m-%d"),
                              timeframe=timeframe)
    if len(df) > 0:
        df = df.reset_index()
        df = df.rename(
            columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume", "Date": "date"})
        df["date"] = pd.to_datetime(df.date)
        df["date"] = df.date.dt.tz_localize(exchange_calendar.tz)
        df["date"] = df.date.dt.tz_convert(datetime.timezone.utc)

        df = df[(df["date"]>=date_from) & (df["date"]<date_to+datetime.timedelta(days=1))]

        df = df.set_index('date', drop=False)
        df['dividend'] = 0
        df['split'] = 0

        df = df[df.date.notnull()]
        df["symbol"] = symbol
        return df
    return df


class LimexHubHistoricalMarketDataProvider(AbstractHistoricalMarketDataProvider):
    def __init__(self, limex_api_key: str, maximum_threads: int | None = None):
        self._limex_api_key = limex_api_key
        self._logger = logging.getLogger(__name__)
        self._limex_client = limexhub.RestAPI(token=limex_api_key)
        if maximum_threads is not None:
            self._maximum_threads = min(multiprocessing.cpu_count() * 2, maximum_threads)
        else:
            self._maximum_threads = multiprocessing.cpu_count() * 2

    def get_historical_data_table(self, symbols: list[str],
                                  period: Period,
                                  date_from: datetime.datetime,
                                  date_to: datetime.datetime,
                                  show_progress: bool,
                                  exchange_calendar: ExchangeCalendar
                                  ):

        def fetch_historical(limex_api_key: str, symbol: str):
            try:
                result = fetch_historical_limex_data_task(date_from=date_from, date_to=date_to,
                                                          exchange_calendar=exchange_calendar,
                                                          limex_api_key=limex_api_key, symbol=symbol, period=period)
                return result
            except Exception as e:
                logging.exception(
                    f"Exception fetching historical data for symbol {symbol}, date_from={date_from}, date_to={date_to}. Skipping."
                )
                return None

        total_days = (date_to - date_from).days
        final = pd.DataFrame()

        if show_progress:
            with progressbar(length=len(symbols) * total_days, label="Downloading historical data from LimexHub",
                             file=sys.stdout) as pbar:
                res = Parallel(n_jobs=self._maximum_threads, prefer="threads",
                               return_as="generator_unordered")(
                    delayed(fetch_historical)(self._limex_api_key, symbol) for symbol in symbols)
                for item in res:
                    pbar.update(total_days)
                    if item is None:
                        continue
                    final = pd.concat([final, item])
        else:
            res = Parallel(n_jobs=self._maximum_threads, prefer="threads", return_as="generator_unordered")(
                delayed(fetch_historical)(self._limex_api_key, symbol) for symbol in symbols)
            for item in res:
                if item is None:
                    continue
                final = pd.concat([final, item])
        final = final.sort_index()
        return final
