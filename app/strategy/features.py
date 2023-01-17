import numpy as np
import pandas as pd

from config import MIDDLE, LONG, LONGEST
from app.utils.downloads import get_snp500


def oscillator(series, window):
    roll = series.rolling(window)
    osc = (series - roll.min()) / (roll.max() - roll.min()) * 100
    return osc


def log_return(df):
    return np.log(df['Close']).diff()


def vwap(df):
    tp = df[['Low', 'High', 'Close']].mean(axis=1)
    vwap = (tp * df['Volume']).rolling(MIDDLE).sum() / \
           df['Volume'].rolling(MIDDLE).sum()
    return vwap


def atr(df):
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(MIDDLE).mean()
    return atr


def adx(df):
    high_diff = df['High'].diff()
    low_diff = -df['Low'].diff()

    df['+DM'] = np.where(high_diff > low_diff, high_diff, 0)
    df['-DM'] = np.where(low_diff > high_diff, low_diff, 0)

    df['+DI'] = (df['+DM'].ewm(span=MIDDLE,
                               min_periods=MIDDLE, adjust=False).mean() / df['ATR']) * 100
    df['-DI'] = (df['-DM'].ewm(span=MIDDLE,
                               min_periods=MIDDLE, adjust=False).mean() / df['ATR']) * 100

    di = np.abs(df['+DI'] - df['-DI']) / \
         np.abs(df['+DI'] + df['-DI']) * 100
    adx = (di.shift() * (MIDDLE - 1) + di) / MIDDLE
    adx = adx.ewm(span=MIDDLE, min_periods=MIDDLE, adjust=False).mean()
    return adx


def ema(df, windows):
    for w in windows:
        df[f'EMA_{w}'] = df['Close'].ewm(
            span=w, adjust=False, min_periods=w).mean()
    return df


def macd(df):
    ewm_12 = df['Close'].ewm(
        span=12, adjust=False, min_periods=12).mean()
    ewm_26 = df['Close'].ewm(
        span=26, adjust=False, min_periods=26).mean()
    df['MACD'] = ewm_12 - ewm_26
    df['MACD_SIG'] = df['MACD'].ewm(
        span=9, adjust=False, min_periods=9).mean()
    #         self.df['MACD_DIFF'] = self.df['MACD'] - self.df['MACD_SIG']
    return df


def rsi(df):
    delta = df['Close'].diff()
    up = delta.clip(lower=0)
    down = delta.clip(upper=0).abs()
    ema_up = up.ewm(span=MIDDLE, adjust=False,
                    min_periods=MIDDLE).mean()
    ema_down = down.ewm(span=MIDDLE, adjust=False,
                        min_periods=MIDDLE).mean()
    rs = ema_up / ema_down
    rsi = 100 - (100 / (1 + rs))
    return rsi


def bollinger_bands(df, k=2):
    sma = df['Close'].rolling(MIDDLE).mean()
    std = df['Close'].rolling(MIDDLE).std()
    df['BB_upper'] = sma + k * std
    df['BB_lower'] = sma - k * std
    return df


def keltner_bands(df):
    ema_20 = df['Close'].ewm(
        span=20, min_periods=20, adjust=False).mean()
    df['KB_upper'] = ema_20 + 2 * df['ATR']
    df['KB_lower'] = ema_20 - 2 * df['ATR']
    return df


def obv(df):
    volumes = np.select(condlist=[df.Close.diff() > 0, df.Close.diff() < 0],
                        choicelist=[df.Volume, -df.Volume])
    return volumes.cumsum()


def money_flow(df):
    df['MFM'] = ((df['Close'] - df['Low'])
                 - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
    df['MFV'] = df['MFM'] * df['Volume']
    df['CMF'] = df['MFM'].rolling(
        21).mean() / df['Volume'].rolling(21).mean()
    df['ADL'] = df['MFV'].cumsum()
    return df


def chaikin_oscillator(df):
    co = df['ADL'].ewm(span=3, min_periods=3, adjust=False).mean() - \
         df['ADL'].ewm(span=10, min_periods=10, adjust=False).mean()
    return co


def generate_features(df):
    """
    Генерирует фичи технических индикаторов
    :param df: OHLC + VOLUME
    """
    # краткая валидация
    _columns = ('Close', 'Open', 'High', 'Low', 'Volume')
    assert all(map(lambda x: x in df.columns, _columns)), \
        f'В dataframe должны быть обязательные колоки {_columns}'
    assert len(df) != 0, "Записи отсутсвуют"

    df = df.copy()
    # Индекс S&P500
    snp500 = get_snp500()
    df = df.join(snp500.loc[df.index])

    # Тех. индикаторы
    df['log_return'] = log_return(df)
    df['VWAP'] = vwap(df)
    df['ATR'] = atr(df)
    df['ADX'] = adx(df)
    df = ema(df, [MIDDLE, LONG, LONGEST])
    df = macd(df)
    df['RSI'] = rsi(df)
    df['StochRSI'] = oscillator(df['RSI'], MIDDLE)
    df = bollinger_bands(df)
    df = keltner_bands(df)
    df['OBV'] = obv(df)
    df = money_flow(df)
    df['Chaikin_osc'] = chaikin_oscillator(df)
    return df
