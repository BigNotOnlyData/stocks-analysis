import logging

import streamlit as st

from app.utils.downloads import get_data


def _input_widgets(block):
    with block:
        # value = st.session_state.get('text_value', '')
        # st.session_state["text"] = ""
        text = st.text_input('Тикер акции',
                               value='',
                               max_chars=7,
                               placeholder='TSLA',
                               key='text',
                               help='Наименование акции на бирже')

        st.slider('Период в годах', 1, 20, key='period', value=1,
                  help="Временной промежуток относительно последней котировки")


def _input_processing(block):
    """
    Обработка входного тикера. Если данные успешно загружены, то сохраняет их.
    :param block: Здесь выводит статус о тикере.
    """
    text = st.session_state.get('text')
    # костыль с тегом <br> для выравнивания по центру input widget
    if not text:
        # Пустая строка
        # st.session_state["df"] = None
        block.write('<br>', unsafe_allow_html=True)
        block.info('Введите тикер', icon="ℹ️")
        logging.info(f'INPUT TEXT: "{text}" - BLANK INPUT')
    elif (df := get_data(text)) is not None:
        # Успешная загрузка данных
        st.session_state["df"] = df
        st.session_state["ticker"] = text.upper()
        block.write('<br>', unsafe_allow_html=True)
        block.success(f'{text}', icon="✔️")
        logging.info(f'INPUT TEXT: "{text}" - OK')
    else:
        # По тикеру данных нет
        st.session_state['df'] = None
        ticker = text if len(text) <= 4 else text[:4] + '...'
        block.write('<br>', unsafe_allow_html=True)
        block.warning(f'{ticker} не найден', icon="⚠️️")
        logging.info(f'INPUT TEXT: "{text}" - NOT DATA')


def set_input_panel(input_block, message_block):
    """
    Загружает данные акции или выводит статус в случае неуспешной загрузки
    :param input_block:
    :param message_block:
    """
    _input_widgets(input_block)
    _input_processing(message_block)
