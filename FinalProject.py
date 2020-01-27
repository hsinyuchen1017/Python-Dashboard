# Please install dash version 0.23.0
# Please install dash_core_components version 1.6.0
# You should also have xlrd to read the excel file.

# Listing down imports
import dash
from dash.dependencies import Input, Output

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as obj

app = dash.Dash(__name__)

# Read the data, so we can create a data frame to work upon.
data_path = "https://s3.amazonaws.com/programmingforanalytics/NBA_data.xlsx"
nba_dataframe = pd.read_excel(data_path)

# Create a data frame which instroe each user's information
data = {}
index = 0
for i in nba_dataframe['Name']:
    data[i] = {}
    for j in nba_dataframe:
        data[i][j] = nba_dataframe[j][index]
    index += 1

# Here we are creating the slider for age of players.
slider = dcc.RangeSlider(id='slider', value=[nba_dataframe['Age'].min(), nba_dataframe['Age'].max()],
                         min=nba_dataframe['Age'].min(), max=nba_dataframe['Age'].max(), step=5,
                         marks={22: '22', 23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29',
                                30: '30', 31: '31', 32: '33', 33: '33', 34: '34'})

# Write a drop-down box, the items come from the column name in the data set
numerical_features = ["Games_played", "Wins", "Losses", "Minutes_played_per_game", "Points_per_game",
                      "Field_goals_made_per_game",
                      "Field_goals_attempted_per_game", "Field_goal_percentage", "3P_made_per_game",
                      "3P_attempted_per_game", "Rebounds_per_game", "Assists_per_game", "Plus_minus", "Salary"]

# Set the drop-down box
options_dropdown = [{'label': x, 'value': x} for x in numerical_features]

# Write the second drop-down box, items come from the column name
numerical_features1 = ['Age', 'Games_played', 'Wins', 'Field_goal_percentage', 'Salary']

# Set the drop-down box
options_dropdown1 = [{'label': x.upper(), 'value': x} for x in numerical_features1]

# Initialize the first drop-down box called options_dropdown, default salary
dd_p1_var = dcc.Dropdown(
    id='performance-var',
    options=options_dropdown,
    value='Salary'
)

# Initialize the second dropdown box called options_dropdown1, default age
# This is the x-axis for scatter plot
dd_x_var = dcc.Dropdown(
    id='x-var',
    options=options_dropdown1,
    value='Age'
)

# Set the hint for choosing x-axis in scatter plot
div_x_var = html.Div(
    children=[html.H4('Variable for x axis: '), dd_x_var],
    # className="six columns"
)

# Initialize the second drop-down box called options_dropdown1, default Games_played
# This is the y-axis for scatter plot
dd_y_var = dcc.Dropdown(
    id='y-var',
    options=options_dropdown1,
    value='Games_played'
)

# Set the hint for choosing y-axis in scatter plot
div_y_var = html.Div(
    children=[html.H4('Variable for y axis: '), dd_y_var],
    className="six columns"
)

# Set the title for histogram
div_p1_var = html.Div(
    children=[html.H4('Select the performance to compare among players: '), dd_p1_var],
    className="six columns"
)

# Format the layout
app.layout = html.Div([

    # Write the title
    html.H1(children='Team_stringr project'),

    # In the tabs, indicate the type of interactive plot
    dcc.Tabs([

        # Interactive scatter plot
        dcc.Tab(label='Interactive scatter plot', children=[
            html.H2(children='Wins and losses of players'),
            html.Div(children='Decide the range by Age to see performance'),
            dcc.Graph(id='player-performance'),
            slider
        ]),

        # Interactive scatter plot 2
        dcc.Tab(label='Interactive scatter plot2', children=[
            html.H1('Scatter plot'),
            html.Div(children=[div_x_var, div_y_var], className="row"),
            dcc.Graph(id='scatter')
        ]),

        # Interactive histogram
        dcc.Tab(label='Interactive histogram plot', children=[
            html.Div(
                children=[div_p1_var],
                className="row"
            ),
            dcc.Graph(id='comparison')

        ]),

        # Interactive selected player intro
        dcc.Tab(label='Interactive selected player introduction', children=[
            html.H2("Introduction of Player", style={'textAlign': 'center'}),
            html.H3("Select Player's name", style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='player_name',
                options=[{'label': i, 'value': i} for i in nba_dataframe['Name']],
                value=nba_dataframe['Name'][0],
                style={'textAlign': 'center', 'width': '250px', 'margin': 'auto'}),
            html.Br(),
            html.Hr(),
            html.Br(),
            html.Div(id='display_selected_player', style={'textAlign': 'center'}),
            html.Br(),
            html.Div(id='display_selected_player_info', style={'textAlign': 'center', 'fontSize': '20px'})
        ]),
    ])
])


@app.callback(Output(component_id='display_selected_player', component_property='children'),
              [Input(component_id='player_name', component_property='value')])
def update_output(value):
    return 'You have selected {}'.format(value)


@app.callback(Output(component_id='display_selected_player_info', component_property='children'),
              [Input(component_id='player_name', component_property='value')])
def update_output2(value):
    return '{} plays for the team {}. His age is {}. He played {} games and won {} games .'.format(value,
                                                                                                   data[value]['Team'],
                                                                                                   data[value]['Age'],
                                                                                                   data[value][
                                                                                                       'Games_played'],
                                                                                                   data[value]['Wins'])


# Using a callback, return the interactive scatter plot the user select
@app.callback(Output('player-performance', 'figure'),
              [Input('slider', 'value')])

# This function will return the scatter plot the user choose
def add_graph(ageslider):
    trace_high = obj.Scatter(
        x=nba_dataframe['Age'],
        y=nba_dataframe['Wins'],
        mode='markers',
        name='Wins')

    trace_low = obj.Scatter(
        x=nba_dataframe['Age'],
        y=nba_dataframe['Losses'],
        mode='markers',
        name='Losses')

    layout = obj.Layout(xaxis=dict(range=[ageslider[0], ageslider[1]]),
                        yaxis={'title': 'Number of Wins/Losses'})

    figure = obj.Figure(data=[trace_high, trace_low], layout=layout)

    return figure


# Using callback, return the interactive scatter plot the user select
@app.callback(
    Output(component_id='scatter', component_property='figure'),
    [Input(component_id='x-var', component_property='value'), Input(component_id='y-var', component_property='value')])
# this function will return the scatter plot the user choose
# it reads two lists and set them as x and y accordingly
def scatter_plot(x_col, y_col):
    trace = obj.Scatter(
        x=nba_dataframe[x_col],
        y=nba_dataframe[y_col],
        mode='markers'
    )

    layout = obj.Layout(
        title='Scatter plot',
        xaxis=dict(title=x_col.upper()),
        yaxis=dict(title=y_col.upper())
    )

    output_plot = obj.Figure(
        data=[trace],
        layout=layout
    )

    return output_plot


# This function will return the histogram plot the user choose
@app.callback(Output(component_id='comparison', component_property='figure'),
              [Input(component_id='performance-var', component_property='value')])
# this function read a list and return a histogram
def histogram(pf):
    trace1 = obj.Histogram(
        x=nba_dataframe[pf],
        name="Players",
        marker=dict(
            color='dodgerblue',
        ),
        opacity=0.75
    )
    data = [trace1]

    # Set the format, such as title, lab, etc
    layout = obj.Layout(
        title='Comparison of performance for players',
        yaxis={"title": 'Counts'},
        bargap=0.2,
        bargroupgap=0.1
    )

    fig = obj.Figure(data=data, layout=layout)
    return fig

# Defining our main
if __name__ == '__main__':
    app.run_server(debug=True)
