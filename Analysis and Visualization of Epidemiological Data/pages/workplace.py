import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go

dash.register_page(__name__)

df_workplace = pd.read_csv('files/workplace.csv')
df_workplace2 = pd.read_csv('files/workplace2.csv')

area_options = [{'label': c, 'value': c} for c in df_workplace['City'].unique()]
year_option = [{'label': i, 'value': i} for i in df_workplace['Year'].unique()]
economic_activities = df_workplace.columns[2:-1]

area_options2 = [{'label': c, 'value': c} for c in df_workplace['City'].unique()]

area_dropdown = dbc.Col(
    [
        html.P('Select Area:', className='fix_label', style={'color': 'black'}),
        dcc.Dropdown(
            id='option_value',
            multi=False,
            value=area_options[0]['value'],
            placeholder='Select Area',
            options=area_options
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
            value=year_option[0]['value'],
            placeholder='Select Year',
            options=year_option
        )
    ],
    md=4,
    sm=12
)

year_dropdown_2 = dbc.Col(
    [
        html.P('Select Year:', className='fix_label', style={'color': 'black'}),
        dcc.Dropdown(
            id='year_value_2',
            multi=False,
            value=year_option[0]['value'],
            placeholder='Select Year',
            options=year_option
        )

    ],
    md=4,
    sm=12
)


area_dropdown_2 = dbc.Col(
    [
        html.P('Select Area:', className='fix_label', style={'color': 'black'}),
        dcc.Dropdown(
            id='option_value_2',
            multi=False,
            value=area_options[0]['value'],
            placeholder='Select Option',
            options=area_options
        )
    ],
    md=4,
    sm=12
)


economic_activities_dropdown =dbc.Col(
    [
        html.P('Select Economic Activities:', className='fix_label', style={'color': 'black'}),
        dcc.Dropdown(
            id='economic_activities_dropdown',
            multi=False,
            value=economic_activities[0],
            placeholder='Select Year',
            options=economic_activities
        )
    ],
    md=4,
    sm=12
)


economic_activities_dropdown_2 =dbc.Col(
    [
        html.P('Select Economic Activities:', className='fix_label', style={'color': 'black'}),
        dcc.Dropdown(
            id='economic_activities_dropdown_2',
            multi=False,
            value=economic_activities[2],
            placeholder='Select Year',
            options=economic_activities
        )
    ],
    md=4,
    sm=12
)

area_dropdown3 = dbc.Col(
    [
        html.P('Select Area:', className='fix_label', style={'color': 'black'}),
        dcc.Dropdown(
            id='option_value3',
            multi=False,
            value=area_options2[0]['value'],
            placeholder='Select Area',
            options=area_options
        )
    ],
    md=4,
    sm=12
)

city_and_year_row = dbc.Row([area_dropdown, year_dropdown])
economic_activities_dropdown_and_year_row_2 = dbc.Row([economic_activities_dropdown, year_dropdown_2])
economic_activities_dropdown_and_area_dropdown_3 = dbc.Row([area_dropdown_2, economic_activities_dropdown_2])




pie_chart_workplace = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="pie_chart_workplace",
                config={'displayModeBar': False},
                style={'height': '600px', 'border': '2px solid #000000'}
            ),
            md=12,
        )
    ]
)

bar_chart_workplace = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="bar_chart_workplace",
                config={'displayModeBar': False},
                style={'height': '600px', 'border': '2px solid #000000'}
            ),
            md=12,
        )
    ]
)

line_chart_workplace = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="line_chart_workplace",
                config={'displayModeBar': False},
                style={'height': '600px', 'border': '2px solid #000000'}
            ),
            md=12,
        )
    ]
)


bar_chart_workplace2 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="bar_chart_workplace2",
                config={'displayModeBar': False},
                style={'height': '600px', 'border': '2px solid #000000'}
            ),
            md=12,
        )
    ]
)


layout = html.Div(children=[city_and_year_row,
                            html.Hr(),
                            pie_chart_workplace,
                            html.Hr(),
                            economic_activities_dropdown_and_year_row_2,
                            html.Hr(),
                            bar_chart_workplace,
                            html.Hr(),
                            economic_activities_dropdown_and_area_dropdown_3,
                            html.Hr(),
                            line_chart_workplace,
                            html.Hr(),
                            area_dropdown3,
                            html.Hr(),
                            bar_chart_workplace2,
                            html.Hr()
                            ])


@callback(
    Output('pie_chart_workplace', 'figure'),
    [Input('option_value', 'value')],
    [Input('year_value', 'value')],

)

def create_pie_chart(option_value, year_value):
    filtered_data = df_workplace[(df_workplace['City'] == option_value) & (df_workplace['Year'] == year_value)]
    labels = filtered_data.columns[2:-1]
    values = filtered_data.iloc[:, 2:-1].values[0]


    fig = go.Figure(data=go.Pie(labels=labels, values=values, hovertemplate="%{label}: %{value} (%{percent})"))

    # Add percentages to the hoverinfo attribute
    fig.update_traces(textinfo='percent+label')

    # Set domain to shift the pie chart to the left
    fig.update_traces(domain=dict(x=[0.2, 0.8]))
    # Add borders around the pie chart slices
    fig.update_traces(marker=dict(line=dict(color='black', width=1)))
    fig.update_layout(title=f'{option_value} {year_value} Economic Activities Distribution', plot_bgcolor='white')

    return fig


@callback(
    Output('bar_chart_workplace', 'figure'),
    [Input('economic_activities_dropdown', 'value')],
    [Input('year_value_2', 'value')],
)

def update_bar_chart(selected_activity, year_value_2):
    filtered_data = df_workplace[df_workplace['Year'] == year_value_2]
    sorted_data = filtered_data.sort_values(selected_activity, ascending=False).head(5)

    fig = go.Figure(
        data=go.Bar(x=sorted_data['City'], y=sorted_data[selected_activity], text=sorted_data[selected_activity],
                    textposition='outside', marker=dict(line=dict(color='black', width=1))))

    # Set custom colors for bars
    colors = px.colors.qualitative.Plotly[:5]
    fig.update_traces(marker=dict(color=colors))

    fig.update_layout(title=f'Top 5 Cities by {selected_activity} in {year_value_2}',
                      xaxis_title='City',
                      yaxis_title=selected_activity,
                      plot_bgcolor='white')

    return fig


@callback(
    Output('line_chart_workplace', 'figure'),
    [Input('option_value_2', 'value')],
    [Input('economic_activities_dropdown_2', 'value')],
)


def create_line_chart(selected_city, selected_activity):
    filtered_data = df_workplace[(df_workplace['City'] == selected_city)]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=filtered_data['Year'], y=filtered_data[selected_activity], mode='lines+markers', name=selected_activity))

    fig.update_layout(title=f'{selected_activity} Trend in {selected_city}',
                      xaxis=dict(title='Year', tickmode='linear', tickvals=df_workplace['Year']),
                      yaxis_title=selected_activity,
                      plot_bgcolor='white')

    return fig


@callback(
    Output('bar_chart_workplace2', 'figure'),
    [Input('option_value3', 'value')],
)

def create_branches_bar_chart(option_value3):
    # Filter the data for the selected city
    city_data = df_workplace2[df_workplace2['City'] == option_value3]

    # Extract the years and the required data for each category
    years = city_data['Year']
    employee_sizes = ['0 to unders 10 employee size', '10 to unders 50 employee size', '50 to under 250 employees size', '250 to more employees size']
    branches_count = city_data[employee_sizes].values.T  # Transpose the data for plotting

    # Create the bar chart
    fig = go.Figure()
    for i, size in enumerate(employee_sizes):
        fig.add_trace(go.Bar(x=years, y=branches_count[i], name=size,text=branches_count[i] ,textposition='outside', marker=dict(line=dict(color='black', width=1))))

    # Update the layout
    fig.update_layout(title=f"Branch Distribution in {option_value3}",
                      xaxis_title="Year",
                      yaxis_title="Number of Branches",
                      showlegend=True,
                      barmode='group',
                      plot_bgcolor='white')

    return fig