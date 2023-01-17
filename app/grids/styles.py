from st_aggrid import JsCode
from config import COLOR_THEME

# цвет ячеек
cellsytle_jscode = JsCode(
    """function(params) {
           return {
               'color': 'white',
               'backgroundColor': 'RGB(0,120,212)'
               } 
        };
    """
    )

# RGB(0,120,212)
# css стили таблицы
AGGRID_CUSTOM_CSS = {
    ".ag-checked": {"background-color": "white !important"},  # цвет галочки
    ".ag-theme-streamlit-dark": {"--ag-alpine-active-color": "RGB(0,120,212)",  # фон чекбокса
                                 "--ag-range-selection-border-color": "RGB(0,120,212)",  # рамка выбранной ячейки
                                 "--ag-input-focus-border-color": "RGB(0,120,212,0.3)",  # подсветка вокруг чекбокса
                                 "--ag-selected-row-background-color": "RGB(0,120,212,0.3)",  # цвет выбранной ячейки
                                 "--ag-row-hover-color": "RGB(0,120,212,0.3)",  # цвет наведения ячеейки
                                 "--ag-checkbox-unchecked-color": "RGB(0,120,212)",  # фон чекбокса невыбранноо
                                 # "--ag-checkbox-background-color": "RGB(255,255,255,0.3)"
                                 },

}
