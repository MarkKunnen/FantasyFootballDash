import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
#https://www.reddit.com/r/fantasyfootball/comments/8y0298/heres_a_spreadsheet_with_10_years_of_fantasy_data/
df = pd.read_csv("fantasy_football.csv")
df.dropna(how='any', inplace=True)
df['Year'] = df['Year'].astype(str)
df = df[df['PPR'] != 0]
df['Position'] = df['FantPos']

# ------------------------------------------------------------------------------
# App layout
app.layout = app.layout = html.Div(
    [
        html.Br(),
        html.H1("Fantasy Football PPR (2014-2018)", style={'text-align': 'left'}),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown('''
                        &nbsp&nbspLooking at the third quartile and above, we can examine **top tier** players by position.
                           * RB have a handful of very strong players each season shown by the outliers in the below boxplot.
                           * WR have far less scarcity when it comes to stronger players.
                           * QB's show a very small gap between the best available and the median.
                           '''),
                        dcc.Graph(id='fig_box', figure={})
                    ]
                ),
                dbc.Col(
                    [
                        html.Div("Select a position"),
                        dcc.Dropdown(id="Position",
                                     options=[
                                         {"label": i, "value": i} for i in df['Position'].unique()],
                                     multi=False,
                                     value='QB',
                                     style={'width': "60%"}
                                     ),
                        html.Div("Top x by position"),
                        dcc.Input(
                            id="Top_x",
                            type="number",
                            value=25),
                        dcc.Graph(id='fig_bar', figure={})
                    ]
                )
            ]
        )
    ]
)

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='fig_box', component_property='figure'),
     Output(component_id='fig_bar', component_property='figure')],
    [Input(component_id='Position', component_property='value'),
     Input(component_id='Top_x', component_property='value')]
)
def update_bar(position, top_x):
    container = "The position chosen by user was: {}".format(position)
    container = "The position chosen by user was: {}".format(position)
    df_copy = df.copy()
    dff = df_copy.sort_values(by='PPR', ascending = False)
    dff['Year_Name'] = dff['Name'] + " (" + dff['Year'] + ")"
    dff = dff[dff["Position"] == position].iloc[:top_x,:].sort_values(by=['Year', 'PPR'])
    fig_bar = px.bar(dff, x='PPR', y='Year_Name', color = 'Year')
    fig_box = px.box(df_copy.sort_values(by='Year'), x='Position', y='PPR', color='Year', hover_data=['Year','Name','PPR'])
    return [fig_box, fig_bar]

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)