import pandas as pd
import streamlit as st

from app.grids import grid_portfolio_assets
from app.utils.settings import set_default_portfolio, clear_text
from .inputs import set_input_panel


def _get_df_portfolio():
    df_portfolio = st.session_state["df_portfolio"]
    if df_portfolio is None:
        df_portfolio = pd.DataFrame(columns=['Date', 'Adj Close', 'Ticker'])
    return df_portfolio


def _add_to_portfolio(df, ticker):
    """
    Добавляет данные об активе в общий датасет портфеля
    :param df: историчесие данные актива
    :param ticker: тикер актива
    """
    df_portfolio = _get_df_portfolio()
    if ticker not in df_portfolio["Ticker"].unique():
        df = df["Adj Close"].reset_index()
        df['Ticker'] = ticker
        st.session_state["df_portfolio"] = pd.concat([df_portfolio, df])


def _format_freq(option):
    if option == 'Y':
        return 'Год'
    elif option == 'Q':
        return 'Квартал'


def portfolio_panel():
    col1, col2, col3, col4 = st.columns([1.98, 1.5, 1, 3], gap='medium')
    set_input_panel(col1, col2)
    if (df := st.session_state["df"]) is not None:
        _add_to_portfolio(df, st.session_state.ticker)

    with col4:
        st.radio("Частота расчётов", ('Y', 'Q'),
                 help="Частота кадров для анимации",
                 key='freq', format_func=_format_freq)

        st.write("<br>", unsafe_allow_html=True)

        if st.button('Сброс', help='Удалить все активы из портфеля', on_click=clear_text):
            set_default_portfolio()

    # Таблица идёт после кнопки для обновления в случае нажатия
    with col3:
        df_portfolio = _get_df_portfolio()
        assets = pd.DataFrame(df_portfolio["Ticker"].unique(),
                              columns=['Активы'])
        selected = grid_portfolio_assets(assets)
        selected_rows = pd.DataFrame(selected["selected_rows"])
        if len(selected_rows) != 0:
            st.session_state['selected_assets'] = selected_rows['Активы'].tolist()
        else:
            st.session_state['selected_assets'] = []

