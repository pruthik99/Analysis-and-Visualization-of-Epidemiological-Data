import dash
import dash_bootstrap_components as dbc
from dash import Dash, html




app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True)

app.layout = html.Div([
    html.Nav([
        html.H1(
            'Epidemiological Data Analysis and Visualization',
            className='navbar-text mx-auto'
        ),
    ],
    className='navbar navbar-expand-lg'),

	 dash.page_container

])

if __name__ == '__main__':
	app.run(debug=True)
	