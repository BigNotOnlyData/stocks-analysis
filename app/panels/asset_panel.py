import streamlit as st

from .inputs import set_input_panel


def asset_panel():
    col1, col2, col3, col4, col5, col6 = st.columns([2, 1.5, 1.3, 0.9, 0.9, 0.9], gap='medium')
    set_input_panel(col1, col2)
    if (df := st.session_state["df"]) is not None:
        with col3:
            ticker = st.session_state["ticker"]
            p = df['Close']
            st.metric(f'{ticker}',
                      value=f"${p.iloc[-1]:.1f}",
                      delta=f"{(p.iloc[-1] - p.iloc[-2]):.2f} ({p.pct_change()[-1]:.2%})")

        for col, w in zip([col4, col5, col6], [200, 65, 5]):
            with col:
                ema = df['Close'].ewm(span=w, adjust=False, min_periods=w).mean()
                st.metric(f'Тренд {w} дней',
                          value=f"${ema.iloc[-1]:.1f}",
                          delta=f"{(ema.iloc[-1] - ema.iloc[-2]):.1f}"
                                f" ({ema.pct_change()[-1]:.2%})")


