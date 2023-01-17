import streamlit as st


def clear_text():
    st.session_state["text"] = ""


def set_default_portfolio():
    st.session_state['selected_assets'] = []
    st.session_state["df_portfolio"] = None


def set_default_session_state():
    if 'selected_assets' not in st.session_state:
        st.session_state['selected_assets'] = []

    if 'df_portfolio' not in st.session_state:
        st.session_state['df_portfolio'] = None

    if 'ticker' not in st.session_state:
        st.session_state['ticker'] = ''

    if 'df' not in st.session_state:
        st.session_state['df'] = None


def _hide_menu():
    """
    Спрятать стримлитовское меню
    """
    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)


def _max_width():
    """
    Макс. ширина: https://stackoverflow.com/questions/70366846/how-can-i-set-layout-size-in-streamlit
    Центрирование: https://stackoverflow.com/questions/17993471/css-wont-center-div-with-max-width
    """
    max_width_str = "max-width: 2000px; margin: 0px auto;"
    html_style = f"""
            <style>
            div.appview-container
            {{{max_width_str}}}
            </style>
            """
    st.markdown(html_style, unsafe_allow_html=True)


def _style_panel_block():
    """
    Панель ввода и краткой информации
    """
    html_style = """
            <style>
            div.css-434r0z.e1tzin5v4 {
            background-color: rgb(20, 21, 26);
            border: 1px solid rgb(38,39,48);
            border-radius: 10px !important;
            padding: 10px}
            </style>
            """
    st.markdown(html_style, unsafe_allow_html=True)


def _style_page_container():
    # css-13mexkk e1tzin5v0
    # css-1ex6qxy.e1tzin5v0
    # css-ocqkz7 e1tzin5v4
    html_style = """
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div >\
                 section > div.block-container.css-k1ih3n.egzxvld4 > div:nth-child(1) >\
                  div > div:nth-child(8) > div {
                /* background-color: rgb(20, 21, 26); */
                border: 1px solid rgb(38,39,48);
                border-radius: 10px !important;
                padding: 10px; 
                /*margin: 10px; */
                }
                </style>
                """
    st.markdown(html_style, unsafe_allow_html=True)


def set_app_config():
    st.set_page_config(page_title="Анализ акций",
                       page_icon="😎",
                       layout="wide")
    _hide_menu()
    _max_width()
    _style_panel_block()
    _style_page_container()
