import yfinance as yf
import streamlit as st
import pandas as pd
import logging
from typing import Optional


def today(func):
    """
    Декоратор для даты конца периода (сегодня).
    Важный параметр для кеширования функции.
    """
    def wrapper(*args, **kwargs):
        data_today = pd.Timestamp.now().strftime('%Y-%m-%d')
        return func(end=data_today, *args, **kwargs)
    return wrapper


@st.cache(max_entries=30, ttl=60*60*12, show_spinner=False)
@today
def get_data(ticker: str, **kwargs) -> Optional[pd.DataFrame]:
    """
    Загрузка котировок акций с yahoo finance
    :param ticker: тикер акции
    """
    # загружаем, если строка не пустая
    data = yf.download(ticker, progress=False, show_errors=True) if ticker else None
    # возвращаем данные, если они есть (случай с несуществующим тикером)
    return data if (data is not None and len(data)) else None


def get_snp500(ticker='SPY') -> pd.Series:
    """
    Загрузка котировок индекса S&P500
    """
    # end_period = pd.Timestamp.now().strftime('%d-%m-%Y')
    sp500 = get_data(ticker)
    sp500 = sp500[['Adj Close']].rename({'Adj Close': 'SP500'}, axis=1)['SP500']
    return sp500


def correction_time_interval(df: pd.DataFrame, years: int, offset: int = 215) -> pd.DataFrame:
    """
    Корректировка интервала для одинаковости периодов стратегии и актива
    (из-за скользящих средних и прочего у стратегии интервал укорачивается)

    :param df: полные данные за все года
    :param years: период рассматриваемых данных
    :param offset: offset == 1 - не смещаем данные, берем указанные период в годах.
    :return: усеченный df
    """

    try:
        end = df.index[-1]
        start = end - pd.DateOffset(years=years)
        new_start = df.loc[df.index <= start][-offset:].index[0]
        return df.loc[new_start:]
    except IndexError:
        logging.warning(f"Не хватает данных для периода {years} годов")
        return df

