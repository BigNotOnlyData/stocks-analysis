import plotly.graph_objects as go
from config import ACTIONS


def plot_positions(df_strategy):
    close = go.Scatter(x=df_strategy.index,
                       y=df_strategy['Close'],
                       mode='lines',
                       marker_color=ACTIONS[0]['color'],
                       opacity=.3,
                       showlegend=False,
                       name='Цена',
                       hovertemplate="%{x}<br>Цена: $%{y:.1f}<extra></extra>",
                       hoverlabel=dict(bgcolor=ACTIONS[0]['color'],
                                       bordercolor='white',
                                       font_color='white')
                       )

    data = [close]
    for pos, df_pos in df_strategy.groupby('position_shifted'):
        if pos == 0:
            continue
        trace = go.Scatter(x=df_pos.index,
                           y=df_pos['Close'],
                           mode='markers',
                           marker_color=ACTIONS[pos]['color'],
                           name=ACTIONS[pos]['name'],
                           hovertemplate="%{x}<br>Цена: $%{y:.1f}",
                           hoverlabel=dict(bgcolor=ACTIONS[pos]['color'],
                                           bordercolor=ACTIONS[pos]['font_color'],
                                           font_color=ACTIONS[pos]['font_color'])
                           )
        data.append(trace)

    layout = go.Layout(template="plotly_dark",
                       xaxis=dict(showline=True,
                                  mirror=True,
                                  linewidth=2,
                                  linecolor='white',
                                  showgrid=False,
                                  title_text="Дата",
                                  ticks="outside",
                                  tickcolor='white'
                                  ),
                       yaxis=dict(title_text='Цена',
                                  showgrid=False,
                                  showline=True,
                                  mirror=True,
                                  linewidth=2,
                                  linecolor='white',
                                  tickformat="$",
                                  zeroline=False),
                       margin=dict(b=5, t=5, pad=0),
                       legend=dict(orientation="h",
                                   yanchor="bottom",
                                   y=1.01,
                                   xanchor="right",
                                   x=1
                                   ),
                       )
    fig = go.Figure(data=data, layout=layout)
    return fig
