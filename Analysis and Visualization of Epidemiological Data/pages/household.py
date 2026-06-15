import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go


dash.register_page(__name__)

df_house = pd.read_csv('files/final_Household_data.csv')

area_options = [{'label': c, 'value': c} for c in df_house['area'].unique()]

area_dropdown = dbc.Col(
    [
        html.P('Select Area Option:', className='fix_label', style={'color': 'black'}),
        dcc.Dropdown(
            id='option_value',
            multi=False,
            value=area_options[0]['value'],
            placeholder='Select Option',
            options=area_options
        )
    ],
    md=4,
    sm=12
)
matrix_dropdown = dbc.Col(
    [
    html.P('Select Matrix Option:', className='fix_label', style={'color': 'black'}),
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': col, 'value': col} for col in df_house.columns[1:-1]],
        value=['Single_Person'],
        multi=True
    )
    ],
    md=4,
    sm=12
)



pie_chart_school1 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="pie_chart_household",
                config={'displayModeBar': False},
                style={'height': '600px', 'border': '2px solid #000000'}
            ),
            md=12,
        )
    ]
)
matrix_chart = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="bar-charts",
                config={'displayModeBar': False},
                style={'height': '600px', 'border': '2px solid #000000'}
            ),
            md=12,
        )
    ]
)
layout = html.Div(children=[matrix_dropdown,
                            html.Hr(),
                            matrix_chart,
                            html.Hr(),
                            area_dropdown,
                            html.Hr(),
                            pie_chart_school1,
                            html.Hr()
                            ])

@callback(
    Output('bar-charts', 'figure'),
    [Input('column-dropdown', 'value')]
)
def display_bar_charts(selected_columns):
    # Sort the data based on the total death count in descending order
    sorted_data = df_house.sort_values('total_Person', ascending=False).head(7)

    # Bar chart for top 10 cities based on total death count
    # colors = ['rgba(100, 150, 200, 0.7)', 'rgba(150, 100, 200, 0.7)', 'rgba(200, 100, 150, 0.7)',
    #           'rgba(100, 200, 150, 0.7)', 'rgba(150, 200, 100, 0.7)', 'rgba(200, 150, 100, 0.7)',
    #           'rgba(100, 200, 200, 0.7)', 'rgba(200, 100, 200, 0.7)', 'rgba(200, 200, 100, 0.7)',
    #           'rgba(150, 150, 150, 0.7)']
    # Stacked bar chart for top 10 cities by age group
    age_groups = sorted_data[selected_columns]  # Exclude 'City', 'Total_Death', and 'Year' columns

    # Grouped bar chart for top 10 cities by age group
    fig3 = go.Figure()
    for age_group in age_groups:
        fig3.add_trace(go.Bar(x=sorted_data['area'], y=sorted_data[age_group],text=sorted_data[age_group], textposition='outside', name=age_group,
        marker=dict(line=dict(color='black', width=1))))
    fig3.update_layout(title=f"Top 7 Cities by Household for {', '.join(selected_columns)}", barmode='group',
                       xaxis_title='City',
                       yaxis_title='Count',
                       plot_bgcolor='white')
    return fig3


@callback(
    Output("pie_chart_household", "figure"),
    [Input("option_value", "value")]
)

def generate_pie_chart(option_value):
    # Filtered data for the selected city
    filtered_data = df_house[df_house['area'] == option_value]

    # Create bar chart for the filtered city
    fig = go.Figure()
    for column in filtered_data.columns[2:]:
        fig.add_trace(go.Bar(x=[column], y=[filtered_data[column].values[0]], name=column, text=[filtered_data[column].values[0]], textposition='outside',
        marker=dict(line=dict(color='black', width=1))))

    fig.update_layout(title=f'{option_value} Household Count by Categories',
                      xaxis_title='Category',
                      yaxis_title='Count',
                      plot_bgcolor='white')

    return fig
