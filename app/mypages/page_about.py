import streamlit as st


def page_about():
    st.subheader("Этапы")
    st.markdown("""
    На всех этапах используется язык программирования Python. 
    + Разработка
        + Формирование отчета актива на основе анализа исторических данных
        + Программирование технических индикаторов
        + Расчёт трейдинговой стратегии
        + Оптимизация активов портфеля
        + Построение графиков
    + Создание веб-сервиса
        + Компоновка результатов с предыдущего этапа в единый сервис
        + Проектирование UI/UX дизайна
    """)

    st.subheader("Данные")
    st.markdown("""Котировки акций загружаются при помощи библиотеки 
    [yfinance](https://pypi.org/project/yfinance/).
    """)

    st.subheader("Визуализация")
    st.markdown("""Для интерактивных графиков используется 
        [plotly](https://plotly.com/python/).
        """)

    st.subheader("Стратегия")
    st.markdown("""
    Для формирования сигнала принятия решения используются технические индикаторы например: 
    *EMA*, *RSI*, *OBV*, *ADX*, *MACD*, *Bollinger Bands* и др. (всего 16). Получая сигнал 
    (*Купить*, *Продать*, *Нейтрал*) от каждого индикатора, формируется результирующий сигнал, 
    который отображается на циферблатном графике.
    """)

    st.subheader("Портфель")
    st.markdown("""
    Доли активов портфеля формируются исходя из максимизации *коэффициента Шарпа* при помощи библиотеки 
    [scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html).
    При этом минимальная доля актива задана 2%.
    """)

    st.subheader("Веб-сервис")
    st.markdown("""
    Сайт спроектирован при помощи [streamlit](https://streamlit.io/), 
    с использованием отдельных компонент 
    [streamlit-aggrid](https://streamlit-aggrid.readthedocs.io/en/docs/AgGrid.html) для таблиц
    и [streamlit_option_menu](https://github.com/victoryhb/streamlit-option-menu) для шапки меню.
    """)
