import numpy as np

from .features import generate_features
from .indicators import indicator_signals, strategy_position


def _form_strategy_data(df_features, position):
    df = df_features.loc[position.index, [
        'Close', 'log_return']]
    df['position_shifted'] = position.shift()
    df = df.dropna()
    df['strategy_return'] = df['log_return'] * df['position_shifted']
    df['return_cumsum'] = df['log_return'].cumsum().apply(np.exp) - 1
    df['strategy_return_cumsum'] = df['strategy_return'].cumsum().apply(np.exp) - 1
    return df


def calculate_strategy(df):
    # создание фичей-индикаторов
    df_features = generate_features(df)
    df_features = df_features.dropna()

    # создание сигналов от индикаторов
    df_signals = indicator_signals(df_features)
    df_signals = df_signals.dropna()

    # определение позиции стратегии
    position = df_signals.apply(strategy_position, axis=1)

    # формирование данных стратегии
    df_strategy = _form_strategy_data(df_features, position)
    return df_strategy, df_signals.iloc[-1]
