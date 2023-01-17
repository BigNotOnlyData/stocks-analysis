import plotly.graph_objects as go

from config import (FILL_COLOR_BUY, COLOR_BUY, COLOR_SELL,
                    FILL_COLOR_SELL, COLOR_FONT_BUY, COLOR_FONT_SELL)


def plot_strategy_return(ret, ret_startegy):
    asset = go.Scatter(x=ret.index, y=ret,
                       fill='tozeroy',
                       mode='lines',
                       fillcolor=FILL_COLOR_SELL,
                       name='Актив',
                       marker_color=COLOR_SELL,
                       hoverlabel=dict(bgcolor=COLOR_SELL,
                                       bordercolor=COLOR_FONT_SELL,
                                       font_color=COLOR_FONT_SELL)
                       )

    strategy = go.Scatter(x=ret_startegy.index, y=ret_startegy,
                          fill='tozeroy',
                          mode='lines',
                          name='Стратегия',
                          marker_color=COLOR_BUY,
                          fillcolor=FILL_COLOR_BUY,
                          hoverlabel=dict(bgcolor=COLOR_BUY,
                                          bordercolor=COLOR_FONT_BUY,
                                          font_color=COLOR_FONT_BUY)
                          )

    layout = go.Layout(template="plotly_dark",
                       hovermode="x",
                       yaxis=dict(showline=True,
                                  mirror=True,
                                  linewidth=2,
                                  linecolor='white',
                                  title_text="Доходность",
                                  tickformat=".0%",
                                  ),
                       xaxis=dict(showline=True,
                                  mirror=True,
                                  linewidth=2,
                                  linecolor='white',
                                  showgrid=False,
                                  title_text="Дата",
                                  ticks="outside",
                                  tickcolor='white'
                                  ),

                       legend=dict(orientation="h",
                                   yanchor="bottom",
                                   y=1.01,
                                   xanchor="right",
                                   x=1
                                   ),
                       margin=dict(b=30, t=30, pad=0),
                       hoverlabel=dict(bgcolor=COLOR_FONT_BUY,
                                       bordercolor='white',
                                       font_color='white'))

    fig = go.Figure(data=[asset, strategy],
                    layout=layout)

    return fig
