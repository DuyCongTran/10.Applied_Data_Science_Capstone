# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
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
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            ],
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
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
                                                marks={0: '0',
                                                    100: '100'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # If ALL sites are selected, use all rows in the dataframe spacex_df
        total_success_by_site = spacex_df[spacex_df['class'] == 1].groupby('Launch Site')['class'].count().reset_index()
        fig = px.pie(total_success_by_site, values='class', names='Launch Site', title='Total Success Launches by Site')
        return fig
    else:
        # If a specific launch site is selected, filter the dataframe spacex_df for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Render and return a pie chart graph to show the success (class=1) count and failed (class=0) count for the selected site
        fig = px.pie(filtered_df, names='class', title=f'Success Launches at {entered_site}')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        # If ALL sites are selected, render a scatter plot to display all values for variable Payload Mass (kg) and variable class.
        # In addition, the point color needs to be set to the booster version i.e., color="Booster Version Category"
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Payload vs Launch Outcome for All Sites',
                         labels={'class': 'Launch Outcome', 'Payload Mass (kg)': 'Payload Mass (kg)'},
                         range_x=payload_range)
        return fig
    else:
        # If a specific launch site is selected, filter the spacex_df first, and render a scatter chart to show
        # values Payload Mass (kg) and class for the selected site, and color-label the point using Booster Version Category likewise.
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'Payload vs Launch Outcome at {selected_site}',
                         labels={'class': 'Launch Outcome', 'Payload Mass (kg)': 'Payload Mass (kg)'},
                         range_x=payload_range)
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
