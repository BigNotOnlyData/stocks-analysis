import logging
import warnings

import streamlit as st
from streamlit_option_menu import option_menu

from app.mypages import page_analysis, page_strategy, page_portfolio, page_about, page_terms
from app.panels import asset_panel, portfolio_panel
from app.utils.settings import set_app_config, set_default_session_state


# https://github.com/victoryhb/streamlit-option-menu
# https://towardsdatascience.com/5-ways-to-customise-your-streamlit-ui-e914e458a17c
# https://medium.com/ssense-tech/streamlit-tips-tricks-and-hacks-for-data-scientists-d928414e0c16
# https://towardsdatascience.com/7-reasons-why-you-should-use-the-streamlit-aggrid-component-2d9a2b6e32f0
# https://streamlit-aggrid.readthedocs.io/en/docs/GridOptionsBuilder.html
# https://discuss.streamlit.io/t/how-to-use-custom-css-in-ag-grid-tables/26743/5
# https://mindspace.ru/abcinvest/kak-oczenit-effektivnost-portfelya-iz-etf/


def app_interface():
    # меню
    page = option_menu(menu_title='Проект по аналитике акций',
                       options=["История", "Стратегия", "Портфель", 'Глоссарий', "О проекте"],
                       icons=['graph-up-arrow', 'yin-yang', "briefcase", 'book', 'lightbulb'],
                       menu_icon="clipboard-data",
                       default_index=0,
                       orientation="horizontal")

    # панель ввода и краткой информации
    if page in {"История", "Стратегия"}:
        asset_panel()
    elif page == "Портфель":
        portfolio_panel()

    # основная информация страницы
    st.header(page)
    with st.container():
        if page == "История":
            page_analysis()
        elif page == "Стратегия":
            page_strategy()
        elif page == "Портфель":
            page_portfolio()
        elif page == "Глоссарий":
            page_terms()
        elif page == "О проекте":
            page_about()


def main():
    try:
        warnings.filterwarnings("ignore")
        set_app_config()
        set_default_session_state()
        app_interface()
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    main()
