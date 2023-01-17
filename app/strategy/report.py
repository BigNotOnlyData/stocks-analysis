import pandas as pd
import numpy as np


def strategy_report(df):
    # общая инфа
    n_trades = (df['position_shifted'] != 0).sum()
    buy_trades = (df['position_shifted'] == 1).sum() / n_trades

    # убытки/прибыль cделок
    s = df['strategy_return']
    profits = s[s > 0]
    losses = s[s < 0]

    hit_ratio = len(profits) / (len(profits) + len(losses))  # win rate

    expected_profits = np.mean(profits)
    expected_losses = np.abs(np.mean(losses))
    total_profits = np.sum(profits)
    total_losses = np.abs(np.sum(losses))
    largest_win = profits.max()
    largest_loss = np.abs(losses).max()
    expectancy = (expected_profits * hit_ratio) \
        - (expected_losses * (1 - hit_ratio))
    realized_risk_reward = expected_profits / expected_losses
    profit_factor = total_profits / total_losses

    # доходность стратегии
    ret = df['strategy_return_cumsum'][-1]
    ret_max = df['strategy_return_cumsum'].max()
    ret_min = df['strategy_return_cumsum'].min()

    # отчет
    data = [('Всего сделок', f'{n_trades}'),
            ('Покупок', f'{buy_trades:.1%}'),
            ('Успешных сделок', f'{hit_ratio:.1%}'),
            ('Средняя прибыль от сделки', f'{expected_profits:.3%}'),
            ("Средние убытки от сделки", f"{expected_losses:.3%}"),
            ("Максимальная прибыль от сделки", f"{largest_win:.2%}"),
            ("Максимальные убытки от сделки", f"{largest_loss:.2%}"),
            ("Ожидаемая доходность от сделки", f"{expectancy:.3%}"),
            ("Коэф. прибыли", f"{profit_factor:.3f}"),
            ("Коэф. риск-вознаграждение", f"{realized_risk_reward:.3f}"),
            ("Максимальная доходность", f"{ret_max:.1%}"),
            ("Минимальная доходность", f"{ret_min:.1%}"),
            ("Совокупная доходность", f"{ret:.1%}")]

    report = pd.DataFrame(data=data, columns=['Параметр', 'Значение'])
    return report
