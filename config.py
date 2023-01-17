
COLOR_THEME = "RGB(0,120,212)"

COLOR_VOLUME = 'rgb(0, 255, 127)'
COLOR_BG_HOVER = 'rgb(9,48,79)'

COLOR_FONT_BUY = 'rgb(68,68,68)'
COLOR_FONT_SELL = 'rgb(255,231,255)'

FILL_COLOR_SELL = 'rgba(255, 0, 255, 0.4)'
FILL_COLOR_BUY = 'rgba(0, 255, 255, 0.4)'

COLOR_SELL = 'rgb(255, 0, 255)'
COLOR_BUY = 'rgb(0, 255, 255)'
COLOR_HOLD = 'rgb(0, 127, 255)'

COLOR_BUY_HOLD = 'rgb(0,170,255)'
COLOR_SELL_HOLD = 'rgb(128,64,255)'

BORDERCOLOR = 'rgb(109, 109, 109)'
ARROWCOLOR = 'rgb(224, 255, 255)'

# Порядок ключей важен
ACTIONS = {-1: dict(name='Продать',
                    color=COLOR_SELL,
                    xdomain=(.2, .4),
                    font_color=COLOR_FONT_SELL),
           0: dict(name='Нейтрал',
                   color=COLOR_HOLD,
                   xdomain=(.4, .6)),
           1: dict(name='Купить',
                   color=COLOR_BUY,
                   xdomain=(.6, .8),
                   font_color=COLOR_FONT_BUY),
           }


SECTOR_ANGLE = [0, 45, 60, 120, 135, 180]
SECTOR_COLORS = [COLOR_SELL,
                 COLOR_SELL_HOLD,
                 COLOR_HOLD,
                 COLOR_BUY_HOLD,
                 COLOR_BUY,
                ]

SECTOR_NAMES = [ACTIONS[-1]['name'],
                f"{ACTIONS[-1]['name']}/{ACTIONS[0]['name']}",
                ACTIONS[0]['name'],
                f"{ACTIONS[1]['name']}/{ACTIONS[0]['name']}",
                ACTIONS[1]['name']]

assert len(SECTOR_ANGLE)-1 == len(SECTOR_COLORS) == len(SECTOR_NAMES), \
    'Цветов и наименований секторов должно быть на одно'\
    'меньше чем углов определяющих секторы'

COLORS_PIE = ['rgb(0, 0, 255)',
              'rgb(0, 128, 255)',
              'rgb(0, 255, 255)',
              'rgb(0, 255, 128)',
              'rgb(224, 255, 255)',
              'rgb(120,162,183)',
              'rgb(128,0,255)',
              'rgb(0,33,55)',
              'rgb(102,0,102)',
              'rgb(53,77,115)',
              'rgb(0,204,150)',
              ]
COLORSCALE = ["rgb(255, 0, 255)",
              "rgb(255, 255, 255)",
              "rgb(0, 255, 255)"]


SHORT = 5
MIDDLE = 14
LONG = 65
LONGEST = 200

DAYS_PER_YEAR = 252

