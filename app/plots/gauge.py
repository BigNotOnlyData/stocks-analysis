import plotly.graph_objects as go
import pandas as pd
import numpy as np

from app.strategy.indicators import strategy_position
from config import SECTOR_ANGLE, SECTOR_COLORS, BORDERCOLOR, ARROWCOLOR, SECTOR_NAMES, ACTIONS


def _arrow_direction(act, signals):
    """
    Определяет отклонение стрелки относительно
    90 градусов в единицах деления циферблата
    """
    if act == 0:
        return signals.sum()
    else:
        return signals.value_counts()[act] * act


def prepare_gauge_params(signals: pd.Series) -> dict:
    """
    Формирует данные для отрисовки циферблата
    """
    ni = len(signals)  # всего индикаторов (делений в половине циферблата)
    act_counts = signals.value_counts().to_dict()
    act = strategy_position(signals)
    ad = _arrow_direction(act, signals)

    # Координаты стрелки
    teta_1 = np.pi / (ni * 2)  # угол одного деления (индикатора)
    teta = (ni - ad) * teta_1  # угол текущей позиции

    r = 0.70
    x = r * np.cos(teta)
    y = r * np.sin(teta)

    # Cекторы
    sector_angle = np.array(SECTOR_ANGLE)
    sector_position = ni * (sector_angle / 90)
    sectors = list(zip(sector_position[:-1], sector_position[1:]))

    steps = [dict(range=[start, stop],
                  color=color,
                  line=dict(color=BORDERCOLOR, width=1))
             for (start, stop), color in zip(sectors, SECTOR_COLORS)]

    # Метки середины секторов
    ticks_angle = sector_angle[:-1] + np.diff(sector_angle) / 2
    ticks_position = ni * (ticks_angle / 90)

    return dict(ni=ni,
                act=act,
                act_counts=act_counts,
                # ad=ad,
                x=x,
                y=y,
                ticks_position=ticks_position,
                steps=steps)


def plot_gauge(ni, act, act_counts, x, y, ticks_position, steps, y_domain=(.35, 1)):
    """
    Отрисовывает датчик принятия решения
    """
    # Циферблат
    gauge = go.Indicator(mode="gauge",
                         domain=dict(x=[0, 1],
                                     y=y_domain),
                         gauge=dict(axis=dict(range=[None, ni * 2],
                                              tickcolor='white',
                                              tickmode='array',
                                              ticktext=SECTOR_NAMES,
                                              tickvals=ticks_position,
                                              tickfont_size=16,
                                              ),
                                    steps=steps,
                                    threshold=dict(line_color='white',
                                                   value=ni),
                                    borderwidth=1,
                                    bar_thickness=0,
                                    bordercolor=BORDERCOLOR
                                    ))
    # Стрелка
    annotations = [dict(ax=0,
                        ay=0,
                        axref='x',
                        ayref='y',
                        x=x,
                        y=y,
                        xref='x',
                        yref='y',
                        showarrow=True,
                        arrowhead=3,
                        arrowsize=1,
                        arrowwidth=5,
                        arrowcolor=ARROWCOLOR,
                        text=f"<b>{ACTIONS[act]['name']}</b>",
                        valign='bottom',
                        yanchor='top',
                        height=50,
                        font_size=26,
                        font_color=ACTIONS[act]['color'],
                        )]
    # Шарнир стрелки
    shapes = [dict(type="circle",
                   xref="x",
                   yref="y",
                   fillcolor="black",
                   line_color=ARROWCOLOR,
                   x0=-0.05,
                   y0=-0.05,
                   x1=0.05,
                   y1=0.05, )]

    # Количественные индикаторы
    summary = [go.Indicator(mode="number",
                            value=act_counts.get(action, 0),
                            domain=dict(x=ACTIONS[action]['xdomain'],
                                        y=[0, .1]),
                            title=ACTIONS[action]['name'],
                            number=dict(font_color=ACTIONS[action]['color']))
               for action in ACTIONS.keys()]

    # Дизайн
    layout = go.Layout(template="plotly_dark",
                       xaxis=dict(showgrid=False,
                                  showticklabels=False,
                                  zeroline=False,
                                  range=[-1, 1],
                                  fixedrange=True,
                                  ),

                       yaxis=dict(showgrid=False,
                                  showticklabels=False,
                                  zeroline=False,
                                  range=[0, 1],
                                  fixedrange=True,
                                  scaleanchor='x',
                                  scaleratio=1,
                                  domain=y_domain),
                       annotations=annotations,
                       margin=dict(b=10),
                       shapes=shapes
                       )
    # график
    fig = go.Figure(data=[gauge, *summary], layout=layout)
    return fig
