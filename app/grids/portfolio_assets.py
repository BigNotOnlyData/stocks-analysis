from st_aggrid import GridOptionsBuilder, AgGrid

from .styles import AGGRID_CUSTOM_CSS


def grid_portfolio_assets(assets):
    """
    Выводит таблицу с возможностью выбрать активы для портфеля.
    """
    gb = GridOptionsBuilder.from_dataframe(assets)
    gb.configure_selection(selection_mode="multiple",
                           use_checkbox=True,
                           pre_selected_rows=list(range(len(assets))),
                           )
    grid_options = gb.build()

    # Костыль для возможности выбрать все активы
    grid_options["columnDefs"][0].update(headerCheckboxSelection=True)

    selected = AgGrid(assets,
                      gridOptions=grid_options,
                      height=160,
                      custom_css=AGGRID_CUSTOM_CSS,
                      allow_unsafe_jscode=True,
                      fit_columns_on_grid_load=True,
                      )
    return selected
