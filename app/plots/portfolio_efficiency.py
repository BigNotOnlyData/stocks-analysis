import plotly.graph_objects as go
import pandas as pd

from config import COLORSCALE, COLORS_PIE, COLOR_BG_HOVER, COLOR_THEME


def plot_portfolio(df: pd.DataFrame) -> go.Figure:
    df = df.copy()

    # Пределы осей для пузырькового графика
    xmin = df['vol'].min()
    xmax = df['vol'].max()
    ymin = df['ret'].min()
    ymax = df['ret'].max()

    k = 0.15  # множитель для увеличения предела осей
    x_min = xmin - k * (xmax - xmin)
    x_max = xmax + k * (xmax - xmin)
    y_min = ymin - k * (ymax - ymin)
    y_max = ymax + k * (ymax - ymin)

    # Пределы цветовой легенды маркеров
    cmax = df['sr'].max()
    cmin = df['sr'].min()

    # Пространство для графиков
    x1_left = 0
    x1_right = 0.5

    x2_left = 0.7
    x2_right = 1

    # Размеры пузырей
    size_min = 10
    size_max = 65

    x_ = df['price']
    df['norm_price'] = ((x_ - x_.min()) / (x_.max() - x_.min())
                        * (size_max - size_min) + size_min)

    # Заголовок круговой диаграммы
    head_pie = dict(font=dict(size=16),
                    showarrow=False,
                    text='Диверсификация портфеля',
                    x=x2_left + ((x2_right - x2_left) / 2),
                    xanchor='center',
                    xref='paper',
                    y=1,
                    yanchor='bottom',
                    yref='paper')

    # Данные для анимации
    slider_steps = []
    frames = []

    for i, (group, df_frame) in enumerate(df.groupby('date')):
        df_frame = df_frame.dropna()
        name = str(group)
        df_pie = df_frame.query("asset != 'Porfolio'")
        df_port = df_frame.query("asset == 'Porfolio'")
        sr, x, y = df_port[['sr', 'vol', 'ret']].squeeze().tolist()

        # Разделение активов и портфеля для отдельной аннотации со
        # стрелкой портфеля и наименовай каждого актива
        scatters = []
        for df_scatter, title in zip([df_pie, df_port],
                                     ['активы', 'портфель']):
            if title == 'активы':
                mode = 'markers+text'
                textposition = "bottom center"
            elif title == 'портфель':
                mode = 'markers'
                textposition = None

            # Пузырьковый график
            scatter = go.Scatter(x=df_scatter['vol'],
                                 y=df_scatter['ret'],
                                 showlegend=False,
                                 mode=mode,
                                 textposition=textposition,
                                 marker=dict(size=df_scatter['norm_price'],
                                             color=df_scatter['sr'],
                                             colorscale=COLORSCALE,
                                             cmax=cmax,
                                             cmin=cmin,
                                             showscale=True,
                                             colorbar=dict(title="К. Шарпа",
                                                           x=x1_right
                                                           ),

                                             ),
                                 text=df_scatter['asset'],
                                 customdata=df_scatter['price'],
                                 hovertemplate="<b>%{text}</b><br><br>" +
                                               "Волатильность: %{x:.1%}<br>" +
                                               "Доходность: %{y:.1%}<br>" +
                                               "Коэф. Шарпа: %{marker.color:.2f}<br>" +
                                               "Цена: %{customdata:$.1f}<br>" +
                                               "<extra></extra>",
                                 hoverlabel=dict(bgcolor=COLOR_BG_HOVER,
                                                 bordercolor='white'
                                                 ),
                                 )
            scatters.append(scatter)

        # Круговая диаграмма
        pie = go.Pie(values=df_pie['weights'],
                     labels=df_pie['asset'],
                     title=f'<span style="font-size: 14px;">Коэф. Шарпа:'
                           f'</span><span style="font-size: 24px;">'
                           f'<br><br><b>{sr:.2f}</b></span>',
                     marker=dict(colors=COLORS_PIE),
                     hole=.6,
                     hovertemplate="<b>%{label}</b><br>Доля: %{percent}",
                     name="",
                     domain=dict(x=[x2_left, x2_right]),
                     # hoverlabel=dict(bgcolor=COLORS_PIE,
                     #                 bordercolor='white')
                     )

        # Аннотация
        portfolio_arrow = dict(x=x,
                               y=y,
                               text='Портфель',
                               showarrow=True,
                               arrowhead=1,
                               )

        # Кадр
        frame = go.Frame(data=[*scatters, pie],
                         name=name,
                         traces=[0, 1, 2],
                         layout=go.Layout(annotations=[head_pie, portfolio_arrow]))

        # Шаг слайдера
        step = dict(args=[[name],
                          dict(mode='immediate',
                               frame=dict(duration=0, redraw=[False, True]),
                               transition=dict(duration=0))],
                    label=name,
                    method="animate",
                    )

        # Сохраняем кадр
        frames.append(frame)
        slider_steps.append(step)

    # Слайдер
    sliders = [dict(steps=slider_steps,
                    x=0.1,
                    y=0,
                    xanchor='left',
                    yanchor='top',
                    pad=dict(t=50, b=10),
                    currentvalue=dict(prefix='Период: ',
                                      xanchor='right',
                                      font=dict(size=20)),
                    len=0.9,
                    tickcolor='#ffffff',
                    tickwidth=1,
                    ticklen=10,
                    )]

    # Кнопки
    updatemenus = [dict(type="buttons",
                        buttons=[dict(label="►",
                                      method="animate",
                                      args=[None,
                                            dict(frame=dict(duration=800,
                                                            redraw=[False, True]),
                                                 fromcurrent=True,
                                                 transition=dict(duration=500,
                                                                 easing="quadratic-in-out"),

                                                 )]),
                                 dict(label="❚❚",
                                      method="animate",
                                      args=[[None],
                                            dict(frame=dict(duration=0,
                                                            redraw=[False, True]),
                                                 mode="immediate",
                                                 transition=dict(duration=0))])
                                 ],
                        showactive=False,
                        bgcolor='black',
                        direction='left',
                        bordercolor=COLOR_THEME,
                        borderwidth=1,
                        font=dict(color=COLOR_THEME),
                        pad=dict(r=20, t=87),
                        x=0.1,
                        y=0,
                        xanchor='right',
                        yanchor='top',
                        )]
    # Дизайн макета
    layout = go.Layout(updatemenus=updatemenus,
                       sliders=sliders,
                       template="plotly_dark",
                       xaxis=dict(range=[x_min, x_max],
                                  title='Волатильность',
                                  domain=[x1_left, x1_right],
                                  showline=True,
                                  mirror=True,
                                  linewidth=2,
                                  linecolor='white',
                                  showgrid=True,
                                  tickformat=".0%"
                                  ),
                       yaxis=dict(range=[y_min, y_max],
                                  title='Доходность',
                                  showline=True,
                                  mirror=True,
                                  linewidth=2,
                                  linecolor='white',
                                  showgrid=True,
                                  tickformat=".0%"
                                  ),
                       legend=dict(title="Активы:",
                                   x=x2_right,
                                   ),
                       annotations=frames[0].layout.annotations,
                       margin=dict(b=5, t=20, pad=0),
                       height=500,
                       # paper_bgcolor='red',
                       )

    # График
    fig = go.Figure(data=frames[0].data,
                    frames=frames,
                    layout=layout
                    )
    return fig
