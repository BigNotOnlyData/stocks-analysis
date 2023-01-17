import logging

import streamlit as st

from app.plots import plot_portfolio
from app.portfolio import calculate_portfolio_data
from app.utils.downloads import correction_time_interval


def page_portfolio():
    try:
        with st.spinner('Загрузка...'):
            # Не рендерим страницу, если выбранных активов нет
            selected_assets = st.session_state.selected_assets
            if not len(selected_assets):
                st.write("Активы не выбраны")
                return

            # подготовка данных для вычисления портфеля
            df = st.session_state["df_portfolio"]
            df = df.pivot_table(values='Adj Close', index='Date', columns='Ticker')
            df = correction_time_interval(df, years=st.session_state['period'], offset=1)
            df = df.loc[:, selected_assets]

            # костыль для помещения графика во внешний DIV для стиля рамки блока
            col, _ = st.columns([1, 0.0001])
            with col:
                # вычисление эффективности активов портфеля
                df_assets = calculate_portfolio_data(df, freq=st.session_state["freq"])
                fig = plot_portfolio(df_assets)
                st.subheader('Эффективность активов')
                st.plotly_chart(fig,
                                use_container_width=True
                                )
    except Exception as e:
        st.write("Не удалось просчитать портфель")
        logging.error(f"'Портфель': {e}")
