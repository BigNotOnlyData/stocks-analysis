import numpy as np
import pandas as pd
from scipy.optimize import minimize, Bounds

from config import DAYS_PER_YEAR


def _port_return(rets, weights):
    return np.dot(rets.mean(), weights) * DAYS_PER_YEAR


def _port_volatility(rets, weights):
    return np.sqrt(np.dot(weights, np.dot(rets.cov() * DAYS_PER_YEAR, weights)))


def _port_sharpe(rets, weights):
    return _port_return(rets, weights) / _port_volatility(rets, weights)


def _optimize_weights(returns: pd.DataFrame, x0: np.array,
                      bounds: Bounds, constraints: dict) -> np.array:
    """
    Оптимизация весов активов в портфеле
    :param returns: доходность активов
    :param x0: начальные веса активов (все равны)
    :param bounds: границы весов
    :param constraints: ограничения (сумма весов равна 1)
    """
    optimal_weights = minimize(fun=lambda weights: -_port_sharpe(returns, weights),
                               x0=x0,
                               method='SLSQP',
                               bounds=bounds,
                               constraints=constraints)["x"]
    return optimal_weights


def calculate_portfolio_data(df: pd.DataFrame, freq='Y', lower_bound=0.02, upper_bound=1.) -> pd.DataFrame:
    """
    Формирует таблицу с портфельными характеристиками
    :param df: таблица у которой колонки это цена отдельног актива
    :param freq: период расчёта
    :param lower_bound: минимальная доля актива в портфеле
    :param upper_bound: максимальная доля актива в портфеле
    """
    df = df.copy()
    df.index = pd.PeriodIndex(df.index, freq=freq)

    bounds = Bounds(lower_bound, upper_bound)
    constraints = {'type': 'eq', 'fun': lambda weights: weights.sum() - 1}

    df_assets = pd.DataFrame()
    for group, df_group in df.groupby(pd.Grouper(freq=freq)):
        # История доходности за период
        returns = np.log(df_group / df_group.shift()).apply('exp') - 1

        # Костыль для определения активов, для которых возможно определять веса и статистики.
        # В какой-то период данных о активе может не быть
        notna_assets = returns.cov().dropna(how='all').index

        n_assets = len(notna_assets)
        if not n_assets:
            continue

        initial = n_assets * [1 / n_assets]

        # Отфильтрованная доходность
        ret = returns[notna_assets]

        # Формируем статистические данные активов
        df_tmp = pd.DataFrame(index=df_group.columns)
        df_tmp['ret'] = ret.mean() * DAYS_PER_YEAR
        df_tmp['vol'] = ret.std() * np.sqrt(DAYS_PER_YEAR)
        df_tmp['sr'] = df_tmp['ret'] / df_tmp['vol']

        # Добавляем оптимальные доли активов
        optimal_weights = _optimize_weights(ret, initial, bounds, constraints)
        df_tmp['weights'] = pd.Series(optimal_weights, index=notna_assets)

        # Добавляем стоимость актива
        df_tmp['price'] = df_group.mean()

        # Добавляем (строку) статистики портфеля (Внимательно с порядком значений)
        df_tmp.loc['Porfolio'] = [_port_return(ret, optimal_weights),
                                  _port_volatility(ret, optimal_weights),
                                  _port_sharpe(ret, optimal_weights),
                                  np.sum(df_tmp['weights']),
                                  np.dot(df_tmp['price'][notna_assets], df_tmp['weights'][notna_assets])
                                  ]

        # Добавляем информацию о группе
        df_tmp['date'] = group

        # Добавляем полученные результаты в итоговую таблицу
        df_assets = pd.concat([df_assets, df_tmp], ignore_index=False)
    return df_assets.reset_index(names='asset')
