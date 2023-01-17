import logging

import streamlit as st

from app.grids import grid_strategy_summary
from app.plots import plot_strategy_return, plot_positions, plot_gauge
from app.plots.gauge import prepare_gauge_params
from app.strategy import strategy_report, calculate_strategy
from app.utils.downloads import correction_time_interval


def page_strategy():
    """
    Страница "Стратегия"
    """
    try:
        with st.spinner('Загрузка...'):
            # Если данных нет, то не рендерим страницу
            df = st.session_state['df']
            if df is None:
                st.write("Данных нет")
                return

            # основная информация
            df = correction_time_interval(df, years=st.session_state['period'], offset=215)
            df_strategy, signals = calculate_strategy(df)

            col1, _, col2 = st.columns([1, .1, 1], gap='small')
            with col1:
                st.subheader("Сигналы на истории")
                fig_sig = plot_positions(df_strategy)
                st.plotly_chart(fig_sig, use_container_width=True)

            with col2:
                st.subheader("Динамика доходности")
                ret = df_strategy['return_cumsum']
                ret_startegy = df_strategy['strategy_return_cumsum']
                fig_ret = plot_strategy_return(ret, ret_startegy)
                st.plotly_chart(fig_ret, use_container_width=True)

            col3, col4 = st.columns([1.1, 1], gap='small')
            with col3:
                st.subheader("Технические индикаторы")
                gauge_params = prepare_gauge_params(signals)
                fig_gauge = plot_gauge(**gauge_params)
                st.plotly_chart(fig_gauge, use_container_width=True)

            with col4:
                st.subheader("Отчёт стратегии")
                report = strategy_report(df_strategy)
                grid_strategy_summary(report)

    except Exception as e:
        st.write("Не удалось просчитать стратегию")
        logging.error(f"'Стратегия': {e}")
