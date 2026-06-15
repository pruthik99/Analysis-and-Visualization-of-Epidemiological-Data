import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc, callback
import plotly.graph_objects as go


dash.register_page(__name__)


df_municipalities = pd.read_csv('files/municipalities.csv')
city_options1 = [{'label': c, 'value': c} for c in df_municipalities['City'].unique()]

year_options1 = [{'label': c, 'value': c} for c in df_municipalities['Year'].unique()]

# District dropdown
city_dropdown = dbc.Col(
    [
        html.P('Select City:', className='fix_label', style={'color': 'black'}),
        dcc.Dropdown(
            id='option_value',
            multi=False,
            value=city_options1[-1]['value'],
            placeholder='Select City',
            options=city_options1
        )
    ],
    md=4,
    sm=12
)

year_dropdown = dbc.Col(
    [
        html.P('Select Year:', className='fix_label', style={'color': 'black'}),
        dcc.Dropdown(
            id='year_value',
            multi=False,
            value=year_options1[-1]['value'],
            placeholder='Select Year',
            options=year_options1
        )
    ],
    md=4,
    sm=12
)

bar_chart_municipalities = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="bar_chart1",
                config={'displayModeBar': False},  # Optional: Hide the mode bar
                style={'height': '600px', 'border': '2px solid #000000'}
            ),
            md=12,
        )
        # Container for information window

    ]
)

bar_chart_top_cities = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="bar_chart_top_cities",
                config={'displayModeBar': False},  # Optional: Hide the mode bar
                style={'height': '600px', 'border': '2px solid #000000'}
            ),
            md=12,
        )
        # Container for information window

    ]
)

layout = html.Div(children=[city_dropdown,
                            html.Hr(),
                            bar_chart_municipalities,
                            html.Hr(),
                            year_dropdown,
                            html.Hr(),
                            bar_chart_top_cities
])

@callback(
    dash.dependencies.Output("bar_chart_top_cities", "figure"),
    [dash.dependencies.Input("year_value", "value")
     ],
)
def generate_bar_chart(selected_year):
    # Filter the data based on the selected year and exclude "Deutschland" and "Rheinland-Pfalz" records
    filtered_data = df_municipalities[(df_municipalities['Year'] == selected_year) & (~df_municipalities['City'].isin(['Deutschland', '  Rheinland-Pfalz']))]

    # Get the top 10 cities by total
    top_10_cities = filtered_data.nlargest(10, 'Total')

    # Create the bar chart using Plotly
    fig = go.Figure(data=go.Bar(x=top_10_cities['City'], y=top_10_cities['Total'], marker=dict(line=dict(color='black', width=1))))

    # Set the chart title and axes labels
    fig.update_layout(
        title=f"Top 10 Cities in {selected_year} for maximum deaths",
        xaxis_title="City",
        yaxis_title="Total",
        plot_bgcolor='white'
    )

    return fig

@callback(
    dash.dependencies.Output("bar_chart1", "figure"),
    [dash.dependencies.Input("option_value", "value")
     ],
)
def linechart(city_value):
    df = df_municipalities[df_municipalities['City'] == city_value]

    # Create the bar chart using Plotly
    fig = go.Figure()

    # Add the bar for total
    fig.add_trace(go.Bar(
        x=df['Year'],
        y=df['Total'],
        name='Total',
        marker_color='#9467bd',
        marker=dict(line=dict(color='black', width=1))
    ))

    # Add the bar for men
    fig.add_trace(go.Bar(
        x=df['Year'],
        y=df['Man'],
        name='Men',
        marker_color='#1f77b4',
        marker=dict(line=dict(color='black', width=1))
    ))

    # Add the bar for women
    fig.add_trace(go.Bar(
        x=df['Year'],
        y=df['Woman'],
        name='Women',
        marker_color='#ff7f0e',
        marker=dict(line=dict(color='black', width=1))
    ))

    # Set the chart title and axes labels
    fig.update_layout(
        title=f"Population by Gender{city_value}",
        xaxis_title='Year',
        yaxis_title='Population',
        plot_bgcolor='white',
        xaxis=dict(
            tickmode='array',
            ticktext=df['Year'],
            tickvals=df['Year']
        )
    )

    return fig





