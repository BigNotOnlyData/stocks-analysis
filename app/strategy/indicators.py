import pandas as pd
import numpy as np


def channel_strategy(series: pd.Series, upper, lower):
    sell = (series > upper).astype(int)
    buy = (series < lower).astype(int)
    signal = buy - sell
    return signal


def quantile_strategy(target, lower, upper, window):
    mean = target.ewm(span=window, min_periods=window, adjust=False).mean()
    signal = channel_strategy(mean, lower=mean.quantile(
        lower), upper=mean.quantile(upper))
    return signal


def stream_candlestick_strategy(low, high, centerline: pd.Series, window=5):
    buy = (low >= centerline).rolling(window).apply(lambda x: np.prod(x))
    sell = (high <= centerline).rolling(window).apply(lambda x: np.prod(x))
    signal = buy - sell
    return signal


def rolling_mean_strategy(series: pd.Series, kind="triple", short=5, middle=15, long=65):
    assert kind in ["double", "triple"], 'Доступный kind: "double", "triple"'
    assert isinstance(series, pd.Series), 'series должен быть pd.Series'

    ema_short = series.ewm(span=short, adjust=False,
                           min_periods=short).mean()
    ema_long = series.ewm(span=long, adjust=False,
                          min_periods=long).mean()

    if kind == "triple":
        ema_middle = series.ewm(span=middle, adjust=False,
                                min_periods=middle).mean()

        buy = ((series >= ema_long) & (ema_short > ema_middle)).astype(int)
        sell = ((series <= ema_long) & (ema_short < ema_middle)).astype(int)

    elif kind == "double":
        sell = (ema_short > ema_long).astype(int)
        buy = (ema_short < ema_long).astype(int)

    signal = buy - sell
    return signal


def adx_signal(adx, pos_di, neg_di, k=25):
    buy = ((adx > k) & (pos_di > neg_di)).astype(int)
    sell = ((adx > k) & (pos_di < neg_di)).astype(int)
    return buy - sell


def ema_signal(features, windows):
    emas = features.columns[[
        c for c in features.columns.str.startswith('EMA_')]]
    df = pd.DataFrame(index=features.index)
    for ema, window in zip(emas, windows):
        suffix = ema.split('_')[-1]
        df[f'EMA_{suffix}'] = stream_candlestick_strategy(
            features['Low'], features['High'], features[ema], window)
    return df


def indicator_signals(features):
    """
    Создаёт сигналы на основе технических индикаторов
    :param features: таблица тех. индикаторов
    """
    df = pd.DataFrame(index=features.index)

    df["SP500"] = rolling_mean_strategy(features['SP500'],
                                        kind="triple",
                                        short=3,
                                        middle=14,
                                        long=65)

    df["VWAP"] = stream_candlestick_strategy(features['Low'],
                                             features['High'],
                                             features["VWAP"],
                                             5)
    df["ADX"] = adx_signal(features["ADX"],
                           features["+DI"],
                           features["-DI"])

    emas = ema_signal(features, windows=[4, 9, 15])
    df = df.join(emas)

    df["Triple_EMA"] = rolling_mean_strategy(features['Close'],
                                             kind="triple",
                                             short=5,
                                             middle=15,
                                             long=65)

    df["MACD"] = channel_strategy(features["MACD"],
                                  features["MACD_SIG"],
                                  features["MACD_SIG"])

    df["RSI"] = channel_strategy(features["RSI"], 70, 30)
    df["StochRSI"] = channel_strategy(features["StochRSI"], 90, 10)

    df["BB"] = channel_strategy(features["Close"],
                                features["BB_upper"],
                                features["BB_lower"])

    df["KB"] = channel_strategy(features["Close"],
                                features["KB_upper"],
                                features["KB_lower"])

    df["OBV"] = rolling_mean_strategy(features['OBV'],
                                      kind="triple",
                                      short=5,
                                      middle=15,
                                      long=65)

    df["MFM"] = quantile_strategy(features['MFM'],
                                  window=15,
                                  lower=.4,
                                  upper=.6)

    df["CMF"] = quantile_strategy(features['CMF'],
                                  window=15,
                                  lower=.2,
                                  upper=.8)

    co = features['Chaikin_osc']
    df["Chaikin_osc"] = channel_strategy(co,
                                         lower=co.quantile(.2),
                                         upper=co.quantile(.8))

    return df


def strategy_position(signals: pd.Series):
    """
    Возвращает действие купить, держать, продать (1, 0, -1)
    signals: серия сигналов индикаторов за один день
    """
    counts = signals.value_counts()
    maximum = counts[counts == counts.max()]
    variants, acts = maximum.shape[0], maximum.index

    # однозначное решение
    if variants == 1:
        return acts[0]
    # балансовое решение
    elif (variants == 3) or (0 not in acts):
        return 0
    # граничное решение
    else:
        return acts[acts != 0][0]


assert strategy_position(pd.Series([1, 1, 1, 0, -1])) == 1
assert strategy_position(pd.Series([1, -1, -1, 0, -1])) == -1
assert strategy_position(pd.Series([1, 1, 0, 0, -1, -1])) == 0
assert strategy_position(pd.Series([1, 1, 1, -1, -1, -1])) == 0
assert strategy_position(pd.Series([0, 0, 0, -1, -1, -1])) == -1
assert strategy_position(pd.Series([1, 1, 1, 1, 1, 1])) == 1
