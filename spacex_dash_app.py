# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
# import dash_html_components as html
# import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': 'All Sites', 'value': 'ALL'},
                                                      {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                      {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                      {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                      {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}],
                                             value='ALL',
                                             placeholder='Select a Launch Site here',
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0Kg', 1000: '1000kg', 2000: '2000kg', 3000: '3000kg',
                                                       4000: '4000kg', 5000: '5000kg', 6000: '6000kg', 7000: '7000kg',
                                                       8000: '8000kg', 9000: '9000kg', 10000: '10000kg'},
                                                value=[min_payload, max_payload]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):

    if entered_site == 'ALL':
        df = spacex_df.groupby('Launch Site', axis=0).count()
        filtered_df = df
        fig = px.pie(filtered_df, values='class',
                     names=filtered_df.index,
                     title='All Launch Site Successes')
    else:
        # return the outcomes piechart for a selected site
        df1 = spacex_df.groupby(['Launch Site', 'class'], axis=0).count().reset_index('class')
        df1['class tag'] = ['Success' if i == 1 else 'Failure' for i in df1['class']]
        filtered_df = df1.loc[entered_site]
        fig = px.pie(filtered_df, values='Flight Number',
                     names='class tag',
                     title='{} Launch Site Success / Failure Rate'.format(str(entered_site)))
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(entered_site, payload):
    if entered_site == 'ALL':
        # apply slider filter to df
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload[0])
                                & (spacex_df['Payload Mass (kg)'] <= payload[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color="Booster Version Category",
                         title='Correlation between Payload and Success for all Sites')
    else:
        # return the outcomes for a selected site
        # apply slider filter to df
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload[0])
                                & (spacex_df['Payload Mass (kg)'] <= payload[1])]
        # apply selected site filter to df
        filtered_df = filtered_df[spacex_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color="Booster Version Category",
                         title='Correlation between Payload and Success for {} Site'.format(str(entered_site)))
    return fig




# Run the app
if __name__ == '__main__':
    app.run_server()



#%%
