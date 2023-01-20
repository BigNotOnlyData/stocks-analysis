# from app.analysis import measure as ms
from . import measure as ms
import pandas as pd

from config import DAYS_PER_YEAR


def asset_report(df):
    # Вычисление показателей
    returns = ms.log_returns(df['Close']).dropna()
    buy_and_hold = returns.cumsum().apply('exp') - 1
    total_return = buy_and_hold[-1]
    best_return = buy_and_hold.max()
    worst_return = buy_and_hold.min()

    period_start = df.index[0]
    period_stop = df.index[-1]
    days = len(df)
    annual_return = ms.cagr(start=1, stop=total_return+1, days=days)
    var = ms.var_hist(returns, level=5)
    cvar = ms.cvar_hist(returns, level=5)

    dd = ms.daily_drawdowns(df['Close'])
    periods_dd = ms.periods_drawdown(dd)
    mdd = dd.min()
    add = dd[dd != 0].mean()
    mdd_duration = periods_dd.sort_values('ddmax')['duration'].iloc[0].days
    add_duration = periods_dd['duration'].mean().days

    sharp = ms.sharpe_ratio(returns)
    sortino = ms.sortino_ratio(returns)
    calmar = ms.calmar_ratio(returns, mdd)

    vol = returns.std()
    vol_annual = vol * (DAYS_PER_YEAR ** .5)
    vol_gain = returns[returns > 0].std()
    vol_loss = returns[returns <= 0].std()

    # Общая информация
    report_general = pd.DataFrame(data={'Параметр': ['Начало',
                                                     'Конец',
                                                     'Торговых дней'],
                                        'Значение': [period_start.strftime('%d-%m-%Y'),
                                                     period_stop.strftime('%d-%m-%Y'),
                                                     days]})
    report_general['Группа'] = 'Период'

    # Доходность
    report_return = pd.DataFrame(data={'Параметр': ['Совокупная',
                                                    'Ежегодная',
                                                    'Лучшая',
                                                    'Худшая'],
                                       'Значение': [f'{total_return:.2%}',
                                                    f'{annual_return:.2%}',
                                                    f'{best_return:.2%}',
                                                    f'{worst_return:.2%}']})
    report_return['Группа'] = 'Доходность'

    # Волатильность
    report_volatility = pd.DataFrame(data={'Параметр': ['Ежегодная',
                                                        'Ежедн. общая',
                                                        'Ежедн. прибыли',
                                                        'Ежедн. убытков'],
                                           'Значение': [f'{vol_annual:.2%}',
                                                        f'{vol:.2%}',
                                                        f'{vol_gain:.2%}',
                                                        f'{vol_loss:.2%}']})
    report_volatility['Группа'] = 'Волатильность'

    # Риски
    report_risk = pd.DataFrame(data={'Параметр': ['Ежедн. макc. потери (VaR, 95%)',
                                                  'Ежедн. наихудшие потери (CVaR, 5%)'],
                                     'Значение': [f'{abs(var):.2%}',
                                                  f'{abs(cvar):.2%}']})
    report_risk['Группа'] = 'Риски'

    # Просадка
    report_drawdowns = pd.DataFrame(data={'Параметр': ['Максимальная',
                                                       'Средняя',
                                                       'Продолжительность (макс.), дни',
                                                       'Продолжительность (сред.), дни'],
                                          'Значение': [f'{abs(mdd):.1%}',
                                                       f'{abs(add):.1%}',
                                                       f'{mdd_duration}',
                                                       f'{int(add_duration)}']})
    report_drawdowns['Группа'] = 'Просадка'

    # Эффективность
    report_efficiency = pd.DataFrame(data={'Параметр': ['Коэф. Шарпа',
                                                        'Коэф. Сортино',
                                                        'Коэф. Кальмара'],
                                           'Значение': [f'{sharp:.2f}',
                                                        f'{sortino:.2f}',
                                                        f'{calmar:.2f}']})
    report_efficiency['Группа'] = 'Эффективность'

    # Итооговый отчет
    df_report = pd.concat([report_general,
                           report_return,
                           report_volatility,
                           report_risk,
                           report_drawdowns,
                           report_efficiency], ignore_index=True)

    df_report = df_report.set_index(['Группа', 'Параметр'])
    df_report = df_report.reset_index()
    return df_report
