import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots


dash.register_page(__name__)

df_covid = pd.read_csv('files/Weekly_covid_data.csv')

area_options = [{'label': c, 'value': c} for c in df_covid['district'].unique()]


area_dropdown = dbc.Col(
    [
        html.P('Select Area:', className='fix_label', style={'color': 'black'}),
        dcc.Dropdown(
            id='option_value_area',
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
        id='column-dropdown_line',
        options=[{'label': col, 'value': col} for col in df_covid.columns[1:-1]],
        value=['total_infection'],
        multi=True
    )
    ],
    md=4,
    sm=12
)

area_dropdown_and_matrix_dropdown = dbc.Row([area_dropdown, matrix_dropdown])


matrix_chart = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="line-charts",
                config={'displayModeBar': False},
                style={'height': '600px', 'border': '2px solid #000000'}
            ),
            md=12,
        )
    ]
)


pie_chart_div = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="pie-charts",
                config={'displayModeBar': False},
                style={'height': '600px', 'border': '2px solid #000000'}
            ),
            md=12,
        )
    ]
)

layout = html.Div(children=[area_dropdown_and_matrix_dropdown,
                            html.Hr(),
                            matrix_chart,
                            html.Hr(),
                            pie_chart_div
                            ])

@callback(
    Output('line-charts', 'figure'),
    [Input('option_value_area', 'value')],
    [Input('column-dropdown_line', 'value')],

)

def create_line_chart(selected_district, selected_columns):
    df_filtered = df_covid[df_covid['district'] == selected_district]

    fig = go.Figure()

    for column in selected_columns:
        # Add the original data as a scatter plot
        fig.add_trace(go.Scatter(x=df_filtered['Week_Number'], y=df_filtered[column].rolling(window=4, min_periods=1).mean(),
                                 mode='markers+lines', name=f'{column} - Original Data'))

    # Update the layout
    fig.update_layout(title=f'Infection Incidence in {selected_district}',
                      xaxis=dict(title='Week Number', tickmode='linear', tickvals=df_filtered['Week_Number']),
                      yaxis_title='Infection Incidence',
                      plot_bgcolor='white',
                      showlegend=True)

    return fig

@callback(
    Output('pie-charts', 'figure'),
    [Input('column-dropdown_line', 'value')],
)
def create_bar_charts(selected_columns):
    df_filtered1 = df_covid[df_covid['district'] != 'Rheinland-Pfalz']
    fig = make_subplots(rows=1, cols=len(selected_columns), subplot_titles=selected_columns, horizontal_spacing=0.1)

    for i, column in enumerate(selected_columns):
        # Calculate the mean for each district
        mean_per_district = df_filtered1.groupby('district')[column].mean()

        # Sort the districts based on the mean value in descending order
        sorted_districts = mean_per_district.sort_values(ascending=False)

        colors = ['rgba(100, 150, 200, 0.7)', 'rgba(150, 100, 200, 0.7)', 'rgba(200, 100, 150, 0.7)',
                  'rgba(100, 200, 150, 0.7)', 'rgba(150, 200, 100, 0.7)', 'rgba(200, 150, 100, 0.7)',
                  'rgba(100, 200, 200, 0.7)', 'rgba(200, 100, 200, 0.7)', 'rgba(200, 200, 100, 0.7)',
                  'rgba(150, 150, 150, 0.7)']

        # Select the top 10 districts
        top_10_districts = sorted_districts.head(10)

        # Add the bar chart for each selected column and top 10 districts
        fig.add_trace(go.Bar(x=top_10_districts.index, y=top_10_districts.values, name=f'{column} - Districts'
                             ,text=top_10_districts.values,textposition='outside',marker=dict(color=colors,line=dict(color='black', width=1))),
                      row=1, col=i + 1)

    # Update the layout for bar charts
    fig.update_layout(title='Top 10 Districts - Infection Incidence',
                      plot_bgcolor='white')

    return fig

