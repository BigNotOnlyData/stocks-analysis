from st_aggrid import AgGrid, ColumnsAutoSizeMode
from .styles import cellsytle_jscode, AGGRID_CUSTOM_CSS


def grid_asset_summary(report):
    grid_options = {
        'columnDefs': [
            {'field': 'Группа', 'rowGroup': True, 'hide': True, },
            {'field': 'Параметр', 'cellStyle': cellsytle_jscode, },
            {'field': 'Значение', 'resizable': True}
        ],

        'groupDefaultExpanded': 1,
        'groupRowsSticky': True,
        'groupDisplayType': 'groupRows',

    }

    AgGrid(report,
           gridOptions=grid_options,
           allow_unsafe_jscode=True,
           custom_css=AGGRID_CUSTOM_CSS,
           columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
           )
