import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import plotly.subplots as sp

dash.register_page(__name__)

df_school = pd.read_csv('files/general_school_data.csv')
df_school['Male'] = df_school['Total_People'] - df_school['Female']

area_options = [{'label': c, 'value': c} for c in df_school['Area'].unique()]


city_dropdown = dbc.Col(
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


school_type_dropdown = dbc.Col(
    [
        html.P('Select School Type:', className='fix_label', style={'color': 'black'}),
        dcc.Dropdown(
            id='School_type',
            multi=False,
            value=area_options[1]['value'],
            placeholder='Select School Type',
            options=[]
        )
    ],
    md=4,
    sm=12
)

city_and_year_row = dbc.Row([city_dropdown, school_type_dropdown])


bar_chart_school1 = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="bar_chart_school",
                config={'displayModeBar': False},
                style={'height': '600px', 'border': '2px solid #000000'}
            ),
            md=12,
        )
    ]
)


line_chart_school = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="line_chart_school",
                config={'displayModeBar': False},
                style={'height': '300px', 'border': '2px solid #000000'}
            ),
            md=12,
        )
    ]
)




layout = html.Div(children=[city_and_year_row,
                            html.Hr(),
                            bar_chart_school1,
                            html.Hr(),
                            line_chart_school
                            ])


@callback(
    Output("bar_chart_school", "figure"),
    [Input("option_value", "value"),
     Input('School_type', 'value')]
)

def linechart1(option_value, School_type):
    df = df_school[(df_school['Area'] == option_value) & (df_school['School_Type'] == School_type)]

    # Create the bar chart using Plotly
    fig = go.Figure()

    # Add the bar for males
    fig.add_trace(go.Bar(
        x=df['Year'],
        y=df['Female'],
        name='Female',
        marker_color='#2ca02c',  # blue color
        text=df['Female'],  # Set text to the male population
        textposition='outside',
        marker=dict(line=dict(color='black', width=1))# Display text outside the bars
    ))
    fig.add_trace(go.Bar(
        x=df['Year'],
        y=df['Male'],
        name='Male',
        marker_color='#1f77b4',  # orange color
        text=df['Male'],  # Set text to the male population
        textposition='outside',
        marker=dict(line=dict(color='black', width=1))#  # Set text position to outside the bar
    ))
    # Add the bar for females
    fig.add_trace(go.Bar(
        x=df['Year'],
        y=df['Foreigners'],
        name='Foreigners',
        marker_color='#9467bd',  # orange color
        text=df['Foreigners'],  # Set text to the male population
        textposition='outside',
        marker=dict(line=dict(color='black', width=1))   # Set text position to outside the bar
    ))

    # Set the chart title and axes labels
    fig.update_layout(
        title=f"Population by Gender - {option_value}",
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

@callback(
    Output('School_type', 'options'),
    [Input('option_value', 'value')]
)
def update_school_type_options(selected_area):
    filtered_school_types = df_school[df_school['Area'] == selected_area]['School_Type'].unique()
    options = [{'label': school_type, 'value': school_type} for school_type in filtered_school_types]
    return options


@callback(
    Output("line_chart_school", "figure"),
    [Input("option_value", "value"),
     Input('School_type', 'value')]
)
def create_dual_line_chart(option_value, School_type):
    df = df_school[(df_school['Area'] == option_value) & (df_school['School_Type'] == School_type)]

    # Create subplots with two columns
    fig = sp.make_subplots(rows=1, cols=2, subplot_titles=('Total People', 'Total Schools'))

    # Add trace for Total People
    fig.add_trace(
        go.Scatter(x=df['Year'], y=df['Total_People'], mode='markers+lines', name='Total People'),
            row=1, col=1
    )

    # Add trace for Total Schools
    fig.add_trace(
        go.Scatter(x=df['Year'], y=df['Total_School'], mode='markers+lines', name='Total Schools'),
        row=1, col=2
    )



    # Update layout
    fig.update_layout(
        title='Trends of Total People and Total Schools over Years',
        xaxis=dict(title='Year', tickmode='linear', tickvals=df['Year']),
        yaxis=dict(title='Count', range=[0, df['Total_People'].max()]),
        xaxis2=dict(title='Year', tickmode='linear', tickvals=df['Year']),
        yaxis2=dict(title='Count', range=[0, df['Total_School'].max()]),
        plot_bgcolor='white',
        showlegend=False
    )

    return fig















