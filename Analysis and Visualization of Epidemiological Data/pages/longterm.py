import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go

dash.register_page(__name__)

df_longterm = pd.read_csv('files/Long_term.csv')
year_option = [{'label': i, 'value': i} for i in df_longterm['Year'].unique()]



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





pie_chart_longterm = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="pie_chart_longterm",
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
                id="bar_chart_longterm",
                config={'displayModeBar': False},
                style={'height': '600px', 'border': '2px solid #000000'}
            ),
            md=12,
        )
    ]
)

layout = html.Div(children=[year_dropdown,
                            html.Hr(),
                            pie_chart_longterm,
                            html.Hr(),
                            bar_chart_workplace,
                            html.Hr()
                            ])


@callback(
    [Output('pie_chart_longterm', 'figure'),
     Output('bar_chart_longterm', 'figure')],
    [Input('year_value', 'value')]
)
def update_charts(selected_year):
    filtered_df = df_longterm[df_longterm['Year'] == selected_year]
    filtered_df1 = filtered_df[filtered_df['Type_of_care'] != 'All kinds of care']


    # Bar chart to show Total_Person, Female, and Male for each Type_of_care
    fig_bar = go.Figure()



    fig_bar.add_trace(go.Bar(
        x=filtered_df1['Type_of_care'],
        y=filtered_df['Female'],
        name='Female',
        marker_color='#ff7f0e',
        text=filtered_df['Female'],  # Display text on top of each bar
        textposition='outside',
        marker=dict(line=dict(color='black', width=1))
    ))

    fig_bar.add_trace(go.Bar(
        x=filtered_df1['Type_of_care'],
        y=filtered_df['Male'],
        name='Male',
        marker_color='#2ca02c',
        text=filtered_df['Male'],  # Display text on top of each bar
        textposition='outside',
        marker=dict(line=dict(color='black', width=1))  # Display text outside the bars
    ))

    fig_bar.update_layout(title=f'Total_Person, Female, and Male for each Type_of_care (Year {selected_year})',
                          xaxis_title='Type of Care',
                          yaxis_title='Count',
                          barmode='group',
                          plot_bgcolor='white',
                          showlegend=True
                          )

    # Pie chart to show the distribution of Total_Person across different types of care
    fig_pie = go.Figure()

    fig_pie.add_trace(go.Pie(
        labels=filtered_df['Type_of_care'],
        values=filtered_df['Total_Person'],
        text=filtered_df['Total_Person'],
        textinfo='label+percent'
    ))
    fig_pie.update_traces(marker=dict(line=dict(color='black', width=1)))

    fig_pie.update_layout(title=f'Distribution of Total_Person across different types of care (Year {selected_year})',
                          plot_bgcolor='white')

    return fig_bar, fig_pie