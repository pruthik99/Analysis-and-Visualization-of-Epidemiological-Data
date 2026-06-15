import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc, callback
import plotly.graph_objects as go


dash.register_page(__name__)


df_death = pd.read_csv('files/death.csv')

df_suicides_death = pd.read_excel('files/Suicides by month of death.xlsx')

df_cancer_death = pd.read_excel('files/cancer.xlsx')

city_options = [{'label': c, 'value': c} for c in df_death['City'].unique()]

year_option = [{'label': i, 'value': i} for i in df_death['Year'].unique()]

# District dropdown
city_dropdown = dbc.Col(
    [
        html.P('Select Area:', className='fix_label', style={'color': 'black'}),
        dcc.Dropdown(
            id='city_value',
            multi=False,
            value=city_options[-1]['value'],
            placeholder='Select Area',
            options=city_options
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
city_and_year_row = dbc.Row([city_dropdown, year_dropdown])

bar_chart = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="bar_chart",
                config={'displayModeBar': False},  # Optional: Hide the mode bar
                style={'height': '600px','border': '2px solid #000000'}
            ),
            md=12,
        )
        # Container for information window

    ]
)
bar_chart_age_group = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="bar_chart_age_group",
                config={'displayModeBar': False},  # Optional: Hide the mode bar
                style={'height': '600px','border': '2px solid #000000'}
            ),
            md=12,
        )
        # Container for information window

    ]
)



layout = html.Div(children=[
                            city_and_year_row,
                            html.Hr(),
                            bar_chart,
                            html.Hr(),
                            bar_chart_age_group,
                            html.Hr()


])


@callback(
    dash.dependencies.Output("bar_chart", "figure"),
    [dash.dependencies.Input("city_value", "value"),
     dash.dependencies.Input('year_value', 'value')
     ],
)


def linechart(city_value, year_value):

    filtered_df = df_death[(df_death['City'] == city_value) & (df_death['Year'] == year_value)]

    # Remove the unnecessary columns
    filtered_df = filtered_df.drop(columns=['City', 'Total_Death', 'Year'])

    # Reshape the DataFrame for plotting
    filtered_df = filtered_df.melt(var_name='Age Group', value_name='Number of Deaths')

    # Create the bar chart using Plotly Express
    color_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                 '#bcbd22', '#17becf', '#1b9e77', '#aec7e8', '#ffbb78', '#ff9896', '#98df8a', '#c5b0d5']

# Create the bar chart using Plotly

    fig = go.Figure(data=go.Bar(
        x=filtered_df['Age Group'],
        y=filtered_df['Number of Deaths'],
        marker_color=color_palette,
        text=filtered_df['Number of Deaths'],
        textposition='outside',
        marker=dict(line=dict(color='black', width=1))
    ))

    # Set the chart title and axes labels
    fig.update_layout(
        title=f"Age Distribution - {city_value} ({year_value})",
        xaxis_title='Age Group',
        yaxis_title='Number of Deaths',
        plot_bgcolor='white'
    )

    return fig

@callback(
    dash.dependencies.Output("bar_chart_age_group", "figure"),
    [dash.dependencies.Input('year_value', 'value')
     ],
)
def generate_charts(selected_year):
    # Filter the data based on the selected year
    filtered_data = df_death[df_death['Year'] == selected_year]

    # Sort the data based on the total death count in descending order
    sorted_data = filtered_data.sort_values('Total_Death', ascending=False).head(5)

    # Bar chart for top 10 cities based on total death count

    # Stacked bar chart for top 10 cities by age group
    age_groups = sorted_data.columns[2:-1]  # Exclude 'City', 'Total_Death', and 'Year' columns

    # Grouped bar chart for top 10 cities by age group
    fig3 = go.Figure()
    for age_group in age_groups:
        fig3.add_trace(go.Bar(x=sorted_data['City'], y=sorted_data[age_group], name=age_group, marker=dict(line=dict(color='black', width=1))))
    fig3.update_layout(title=f'Top 5 Cities by Death Count in Age Groups ({selected_year})', barmode='group',
                       xaxis_title='City',
                       yaxis_title='Number of Deaths',
                       plot_bgcolor='white')

    return fig3


