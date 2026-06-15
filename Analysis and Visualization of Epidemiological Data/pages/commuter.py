import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

dash.register_page(__name__)

df_commuter = pd.read_excel('files/commuter data.xlsx')
df_commuter['Total under 25'] = df_commuter['total'] - df_commuter['total_25_to_45'] - df_commuter['total_45_to_67']
df_commuter['Man under 25'] = df_commuter['total_man'] - df_commuter['man_under_45'] - df_commuter['man_45_to_67']
df_commuter['Female under 25'] = df_commuter['total_female'] - df_commuter['female_under_45'] - df_commuter['female_45_to_67']

column_mapping = {
    'total': 'Total',
    'total_25_to_45': 'Total 25 to 45',
    'total_45_to_67': 'Total 45 to 67',
    'total_man': 'Total Man',
    'man_under_45': 'Man 25 to 45',
    'man_45_to_67': 'Man 45 to 67',
    'total_female': 'Total Female',
    'female_under_45': 'Female 25 to 45',
    'female_45_to_67': 'Female 45 to 67',
}

# Rename columns using the dictionary
df_commuter.rename(columns=column_mapping, inplace=True)

area_options = [{'label': c, 'value': c} for c in df_commuter['district'].unique()]


area_dropdown = dbc.Col(
    [
        html.P('Select Area:', className='fix_label', style={'color': 'black'}),
        dcc.Dropdown(
            id='option_value_commuter',
            multi=False,
            value=area_options[0]['value'],
            placeholder='Select Option',
            options=area_options
        )
    ],
    md=4,
    sm=12
)

bar_chart_commuter = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="bar_chart_commuter",
                config={'displayModeBar': False},
                style={'height': '600px', 'border': '2px solid #000000'}
            ),
            md=12,
        )
    ]
)


layout = html.Div(children=[area_dropdown,
                            html.Hr(),
                            bar_chart_commuter

                            ])

@callback(
    Output('bar_chart_commuter', 'figure'),
    Input('option_value_commuter', 'value'),

)

def create_subplot_figure(option_value_commuter):
    selected_row = df_commuter[df_commuter["district"] == option_value_commuter]

    # Extract the required data for each sub chart
    total_data = selected_row[['Total', 'Total under 25', 'Total 25 to 45', 'Total 45 to 67']].values[0]
    male_data = selected_row[['Total Man', 'Man under 25', 'Man 25 to 45', 'Man 45 to 67']].values[0]
    female_data = selected_row[['Total Female', 'Female under 25', 'Female 25 to 45', 'Female 45 to 67']].values[0]

    # Create subplots with one row and three columns
    fig = make_subplots(rows=1, cols=3, subplot_titles=('Total', 'Male', 'Female'))

    # Add the bar chart for Total data
    fig.add_trace(go.Bar(x=['Total', 'Under 25', '25 to 45', '45 to 67'], y=total_data, name='Total',text=total_data ,textposition='outside', marker=dict(line=dict(color='black', width=1))), row=1, col=1)

    # Add the bar chart for Male data
    fig.add_trace(go.Bar(x=['Total', 'Under 25', '25 to 45', '45 to 67'], y=male_data, name='Male',text=male_data, textposition='outside', marker=dict(line=dict(color='black', width=1))), row=1, col=2)

    # Add the bar chart for Female data
    fig.add_trace(go.Bar(x=['Total', 'Under 25', '25 to 45', '45 to 67'], y=female_data, name='Female',text=female_data, textposition='outside', marker=dict(line=dict(color='black', width=1))), row=1, col=3)

    # Update the layout
    fig.update_layout(title=f'Distribution in {option_value_commuter}',
                      xaxis=dict(title='Age Groups'),
                      yaxis=dict(title='Count'),
                      plot_bgcolor='white',
                      showlegend=False)


    return fig



