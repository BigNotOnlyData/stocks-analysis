import logging

import streamlit as st

from app.analysis.measure import daily_drawdowns
from app.analysis import asset_report
from app.grids import grid_asset_summary
from app.plots import plot_drawdown, plot_ohlc
from app.utils.downloads import correction_time_interval


def page_analysis():
    """
    Страница "История"
    """
    try:
        with st.spinner('Загрузка...'):
            # Если данных нет, то не рендерим страницу
            df = st.session_state['df']
            if df is None:
                st.write("Данных нет")
                return

            # основная информация
            df = correction_time_interval(df, years=st.session_state['period'], offset=1)
            col1, _, col2 = st.columns([2, .1, 1], gap='small')
            with col1:
                st.subheader("OHLC")
                fig_ohlc = plot_ohlc(df)
                st.plotly_chart(fig_ohlc, use_container_width=True)

                st.subheader("Просадка")
                dd = daily_drawdowns(df['Close'])
                fig_dd = plot_drawdown(dd)
                st.plotly_chart(fig_dd, use_container_width=True)

            with col2:
                st.subheader('Сводная информация')
                report = asset_report(df)
                grid_asset_summary(report)

    except Exception as e:
        st.write("Не удалось просчитать историю")
        logging.error(f"'История': {e}")
