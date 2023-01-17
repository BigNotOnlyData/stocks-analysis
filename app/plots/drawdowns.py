import plotly.graph_objects as go
import config as cf


def plot_drawdown(dd):
    drawdown = go.Scatter(x=dd.index,
                          y=dd.abs(),
                          fill='tozeroy',
                          mode='lines',
                          fillcolor=cf.FILL_COLOR_SELL,
                          marker_color=cf.COLOR_SELL,
                          name='',
                          hovertemplate="%{y:.1%}",
                          )
    layout = go.Layout(template="plotly_dark",
                       yaxis=dict(showline=True,
                                  mirror=True,
                                  linewidth=2,
                                  linecolor='white',
                                  title_text="Просадка",
                                  tickformat=".0%",
                                  autorange='reversed'
                                  ),
                       xaxis=dict(showline=True,
                                  mirror=True,
                                  linewidth=2,
                                  linecolor='white',
                                  showgrid=False,
                                  title_text="Дата",
                                  ticks="outside",
                                  tickcolor='white',
                                  hoverformat='<b>%e %b %Y (%a)</b>',
                                  spikecolor="white",
                                  ),

                       margin=dict(b=5, t=5, pad=0),
                       hovermode="x unified",
                       hoverlabel=dict(bgcolor=cf.COLOR_BG_HOVER,
                                       bordercolor='white'
                                       ),
                       # width=500,
                       height=300,
                       )

    fig = go.Figure(data=[drawdown], layout=layout)
    return fig
