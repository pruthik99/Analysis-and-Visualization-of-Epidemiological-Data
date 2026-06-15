import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State

dash.register_page(__name__, path='/')


first_card = dbc.Card([
    dbc.CardBody(
        [

            html.H5("Work Place Data", className="card-title text-center"),


        ], style={'height': '150px'}
    ),
        dbc.CardFooter([
            dcc.Location(id='url_municipalities', refresh=True),
            dbc.Button("Go", id="button_dashboard", color="success")
            ], style={'text-align': 'center'}),

])

@callback(
    Output('url_municipalities', 'pathname'),
    [Input('button_dashboard', 'n_clicks')],
    [State('url_municipalities', 'pathname')],
)
def navigate_to_app(n_clicks, pathname):
    if n_clicks:
        return '/workplace'
    return pathname






second_card = dbc.Card([
    dbc.CardBody(
        [
            html.H5("Death Data", className="card-title text-center"),

        ],  style={'height': '150px'}
    ), dbc.CardFooter([
                    dcc.Location(id='url_death', refresh=True),
                    dbc.Button("Go", id='button_assessment', color="success")
    ], style={'text-align': 'center'})
])

@callback(
    Output('url_death', 'href'),
    [Input('button_assessment', 'n_clicks')],
    [State('url_death', 'href')],
)
def navigate_to_app(n_clicks, href):
    if n_clicks:
        return '/death'
    return href



#--------------------------------------------------------------------------


third_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H5("General Education School Data", className="card-title text-center"),
            ],
            style={'height': '150px'}
        ),
        dbc.CardFooter(
            [
                dcc.Location(id='url_general_school', refresh=True),
                dbc.Button("Go", id='button_general_school', color="success")
            ], style={'text-align': 'center'}
        )
    ]
)
@callback(
    Output('url_general_school', 'pathname'),
    [Input('button_general_school', 'n_clicks')],
    [State('url_general_school', 'pathname')],
)
def navigate_to_general_school(n_clicks, pathname):
    if n_clicks:
        return '/generalschool'
    return pathname


# ---------------------------------------------------------------------------------


fourth_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H5("Household Data", className="card-title text-center"),
            ],
            style={'height': '150px'}
        ),
        dbc.CardFooter(
            [
                dcc.Location(id='url_household data', refresh=True),
                dbc.Button("Go", id='button_household data', color="success")
            ], style={'text-align': 'center'}
        )
    ]
)

@callback(
    Output('url_household data', 'pathname'),
    [Input('button_household data', 'n_clicks')],
    [State('url_household data', 'pathname')],
)
def navigate_to_new_card(n_clicks, pathname):
    if n_clicks:
        return '/household'
    return pathname


# ------------------------------------------------------------------------

sixth_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H5("Vocational School Data", className="card-title text-center"),
            ],
            style={'height': '150px'}
        ),
        dbc.CardFooter(
            [
                dcc.Location(id='url_vocational_data', refresh=True),
                dbc.Button("Go", id='button_vocational_data', color="success")
            ], style={'text-align': 'center'}
        )
    ]
)

@callback(
    Output('url_vocational_data', 'pathname'),
    [Input('button_vocational_data', 'n_clicks')],
    [State('url_vocational_data', 'pathname')],
)
def navigate_to_new_card(n_clicks, pathname):
    if n_clicks:
        return '/vocational'
    return pathname


# ----------------------------------------------

seventh_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H5("Long Term Health Care Facilities Data", className="card-title text-center"),

            ],
            style={'height': '150px'}
        ),
        dbc.CardFooter(
            [
                dcc.Location(id='url_care_data', refresh=True),
                dbc.Button("Go", id='button_care_data', color="success")
            ], style={'text-align': 'center'}
        )
    ]
)

@callback(
    Output('url_care_data', 'pathname'),
    [Input('button_care_data', 'n_clicks')],
    [State('url_care_data', 'pathname')],
)
def navigate_to_new_card(n_clicks, pathname):
    if n_clicks:
        return '/longterm'
    return pathname

# -----------------------------------------------------------------------------------
card_number_eight = dbc.Card([
    dbc.CardBody(
        [

            html.H5("Covid Data", className="card-title text-center"),

        ], style={'height': '150px'}
    ),
        dbc.CardFooter([
            dcc.Location(id='url_covid', refresh=True),
            dbc.Button("Go", id="button_covid", color="success")
            ], style={'text-align': 'center'}),

])

@callback(
    Output('url_covid', 'pathname'),
    [Input('button_covid', 'n_clicks')],
    [State('url_covid', 'pathname')],
)
def navigate_to_app(n_clicks, pathname):
    if n_clicks:
        return '/covid'
    return pathname


card_number_nine = dbc.Card([
    dbc.CardBody(
        [

            html.H5("Commuter Data", className="card-title text-center"),

        ], style={'height': '150px'}
    ),
        dbc.CardFooter([
            dcc.Location(id='url_commuter', refresh=True),
            dbc.Button("Go", id="button_commuter", color="success")
            ], style={'text-align': 'center'}),

])

@callback(
    Output('url_commuter', 'pathname'),
    [Input('button_commuter', 'n_clicks')],
    [State('url_commuter', 'pathname')],
)
def navigate_to_app(n_clicks, pathname):
    if n_clicks:
        return '/commuter'
    return pathname




first_row = dbc.Row(
    [
        dbc.Col(first_card, width=3,style={'margin-left': '1.5rem', 'margin-right': '1.5rem'}),
        dbc.Col(second_card, width=3,style={'margin-left': '1.5rem', 'margin-right': '1.5rem'}),
        dbc.Col(third_card, width=3,style={'margin-left': '1.5rem', 'margin-right': '1.5rem'})
    ], className="mt-5 justify-content-center"
    )

second_row = dbc.Row(
    [
    dbc.Col(fourth_card, width=3, style={'margin-left': '1.5rem', 'margin-right': '1.5rem'}),
    dbc.Col(sixth_card, width=3, style={'margin-left': '1.5rem', 'margin-right': '1.5rem'}),
    dbc.Col(seventh_card, width=3, style={'margin-left': '1.5rem', 'margin-right': '1.5rem'}),

    ],
    className="mt-5 mb-5 justify-content-center"  # Added mt-5 class for more margin-top
)

third_raw = dbc.Row(
    [
    dbc.Col(card_number_eight, width=3, style={'margin-left': '1.5rem', 'margin-right': '1.5rem'}),
    dbc.Col(card_number_nine, width=3, style={'margin-left': '1.5rem', 'margin-right': '1.5rem'}),
    ],
    className="mt-5 mb-5 justify-content-center"  # Added mt-5 class for more margin-top
)





layout = html.Div(children=[
    first_row,
    second_row,
    third_raw
])

