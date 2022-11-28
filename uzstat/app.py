
import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(
    'database',
    external_stylesheets=external_stylesheets
)
app.config.suppress_callback_exceptions = True
app.title = 'параметры работы мельницы'
app.description = """параметры работы цементной мельницы"""
server = app.server
