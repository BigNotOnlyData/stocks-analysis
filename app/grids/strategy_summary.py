from st_aggrid import AgGrid

from .styles import cellsytle_jscode, AGGRID_CUSTOM_CSS


def grid_strategy_summary(report):
    grid_options = {
        'columnDefs': [
            {'field': 'Параметр', 'cellStyle': cellsytle_jscode, },
            {'field': 'Значение'}
        ],

    }

    AgGrid(report,
           gridOptions=grid_options,
           allow_unsafe_jscode=True,
           custom_css=AGGRID_CUSTOM_CSS,
           fit_columns_on_grid_load=True,
           )
