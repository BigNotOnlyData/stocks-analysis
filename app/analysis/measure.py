from typing import Union

import numpy as np
import pandas as pd

from config import DAYS_PER_YEAR


def log_returns(price: pd.Series) -> pd.Series:
    """
    Логарифмическая доходность актива
    """
    return np.log(price).diff()


def cagr(start: Union[int, float], stop: Union[int, float], days: int) -> float:
    """
    Cреднегодовой темп роста
    :param start: начальное значение величины
    :param stop: конечное значение величины
    :param days: кол-во пройденных дней
    """
    return (stop / start) ** (DAYS_PER_YEAR / days) - 1.0


def var_hist(returns: pd.Series, level: int = 5) -> float:
    """
    Максимальными потери, которые вы можете иметь в (100 - level)% случаев
    """
    return np.percentile(returns, level)


def cvar_hist(returns: pd.Series, level: int = 5) -> float:
    """
    Наихудшая доходность
    """
    is_beyond = returns <= var_hist(returns, level)
    return returns[is_beyond].mean()


def sharpe_ratio(returns: pd.Series, rf: float = .0) -> float:
    """
    Коэффициент Шарпа
    :param returns: доходность
    :param rf: безрисковая процентная ставка
    """
    mean = returns.mean() * DAYS_PER_YEAR - rf
    sigma = returns.std() * np.sqrt(DAYS_PER_YEAR)
    return mean / sigma


def sortino_ratio(returns: pd.Series, rf: float = .0) -> float:
    """
    Коэффициент Сортино
    :param returns: доходность
    :param rf: безрисковая процентная ставка
    """
    mean = returns.mean() * DAYS_PER_YEAR - rf
    std_neg = returns[returns < 0].std() * np.sqrt(DAYS_PER_YEAR)
    return mean / std_neg


def calmar_ratio(returns: pd.Series, max_drawdown: float, rf: float = .0) -> float:
    """
    Коэффициент Сортино
    :param returns: доходность
    :param max_drawdown: максимальная просадка
    :param rf: безрисковая процентная ставка
    """
    mean = returns.mean() * DAYS_PER_YEAR - rf
    return mean / abs(max_drawdown)


def daily_drawdowns(price: pd.Series) -> pd.Series:
    """
    Ежедневная просадка
    :param price: цена
    """
    roll_max = price.cummax()
    daily_drawdown = price / roll_max - 1.0
    return daily_drawdown


def periods_drawdown(dd: pd.Series) -> pd.DataFrame:
    """
    Рассчитывает продолжительность периодов просадок
    :param dd: Ежедневная просадка
    """
    dd_zero = dd[dd == 0]
    dd_zero.loc[dd.index[-1]] = 0  # добавим 0 в конец для текущей просадки

    periods_dd = pd.DataFrame(columns=['start', 'stop', 'ddmax'])

    for date_start, date_stop in zip(dd_zero.index[:-1], dd_zero.index[1:]):
        local_max = dd.loc[date_start:date_stop].min()
        periods_dd.loc[len(periods_dd)] = [date_start, date_stop, local_max]

    periods_dd['duration'] = periods_dd['stop'] - periods_dd['start']
    return periods_dd
