import plotly.graph_objects as go
import pandas as pd

from config import COLOR_BG_HOVER, COLOR_BUY, COLOR_SELL, COLOR_VOLUME


def plot_ohlc(df: pd.DataFrame) -> go.Figure:
    # Свечной график
    candlestick = go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 yaxis="y2",
                                 increasing_line_color=COLOR_BUY,
                                 decreasing_line_color=COLOR_SELL,
                                 name='',
                                 yhoverformat="$.1f"
                                 )

    # График объема
    volume = go.Bar(x=df.index,
                    y=df.Volume,
                    marker_color=COLOR_VOLUME,
                    opacity=0.6,
                    name='',
                    hovertemplate='<br>volume: %{y:.3s}<br>'
                    )


    # Дизайн
    layout = go.Layout(template="plotly_dark",
                       showlegend=False,
                       margin=dict(b=5, t=5, pad=0),
                       xaxis=dict(title='Дата',
                                  rangeslider_visible=False,
                                  hoverformat='<b>%e %b %Y (%a)</b>',
                                  spikecolor="white",
                                  showline=True,
                                  mirror=True,
                                  linewidth=2,
                                  linecolor='white',
                                  ticks="outside",
                                  tickcolor='white'
                                  ),
                       yaxis=dict(title='Объем',
                                  side='right',
                                  titlefont=dict(color=COLOR_VOLUME),
                                  tickfont=dict(color=COLOR_VOLUME),
                                  showgrid=False,
                                  zeroline=False,
                                  fixedrange=True,
                                  showline=True,
                                  linewidth=2,
                                  linecolor='white',),
                       yaxis2=dict(title='Цена',
                                   side='left',
                                   overlaying='y',
                                   anchor="x",
                                   titlefont=dict(color=COLOR_BUY),
                                   tickfont=dict(color=COLOR_BUY),
                                   tickformat="$",
                                   showline=True,
                                   linewidth=2,
                                   linecolor='white',),

                       hovermode="x unified",
                       hoverlabel=dict(bgcolor=COLOR_BG_HOVER,
                                       bordercolor='white'
                                       ),
                       # width=500,
                       # height=600,
                       )

    fig = go.Figure(data=[volume, candlestick],
                    layout=layout)
    return fig
