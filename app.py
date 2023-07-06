import dash
import dash_bootstrap_components as dbc
from layout import get_layout
import callbacks as app_callbacks


def set_up_dash_app() -> dash.Dash:
    '''Set up and return a dash app.'''
    external_stylesheets = [
        'https://codepen.io/chriddyp/pen/bWLwgP.css',
        dbc.themes.BOOTSTRAP]
    dash_app = dash.Dash(
        title='Visualization Board',
        external_stylesheets=external_stylesheets,
    )
    dash_app.layout = get_layout()
    # set_up_dash_basic_auth(dash_app)
    return dash_app


app = set_up_dash_app()
