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
server = app.server

app.title = "SpaceX Launch Records Dashboard"
launch_sites = spacex_df['Launch Site'].unique()
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}]
for site in launch_sites:
    dropdown_options.append(
    {'label': site, 'value': site},
    )
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                
                                dcc.Dropdown(id='site-dropdown',
                                            options=dropdown_options ,
                                            value='ALL',
                                            placeholder='Select a Launch Site',
                                            searchable=True
                                            #style={'width':'80%', 'padding':'3px','font-size': '20px','textAlign':'center'}
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
                                                    2500: '2500',
                                                    5000: '5000',
                                                    7500: '7500',
                                                    10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    data = spacex_df[['Launch Site', 'class']]
    data_group1 = data.groupby(['Launch Site'])['class'].sum().reset_index()
    if entered_site == 'ALL':
        fig = px.pie(data_group1, values='class', 
        names='Launch Site', 
        title='Successful Launches By Site')
        return fig
    else:
        filtered_data = data[data['Launch Site'] == entered_site]
        data_grouped = filtered_data.groupby(['class'])['Launch Site'].count().reset_index()
        fig = px.pie(data_grouped, values='Launch Site', 
        names='class', 
        title=f'Launch Results For Site {entered_site}')
        return fig        

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_plot(entered_site, payload_range):
    start, end = payload_range
    data1 = spacex_df[['Launch Site','Payload Mass (kg)', 'class', 'Booster Version Category']]
    if entered_site == 'ALL':
        filtered_data1 = data1[(data1['Payload Mass (kg)'] >= start) & (data1['Payload Mass (kg)'] <= end) ]
        fig = px.scatter(filtered_data1, 
                         x= 'Payload Mass (kg)', 
                         y='class',
                         color = 'Booster Version Category',
                         title='Correlation between payload and success for all sites')
#        fig.update_layout(xaxis=dict(
#            rangeslider=dict(visible=True)
#        ))
        return fig
    else:
        filtered_data1 = data1[(data1['Launch Site'] == entered_site) & (data1['Payload Mass (kg)'] >= start) & (data1['Payload Mass (kg)'] <= end) ]
        
        fig = px.scatter(filtered_data1, 
                    x= 'Payload Mass (kg)', 
                    y='class',
                    color = 'Booster Version Category',
                    title=f'Correlation between payload and success For Site {entered_site}')

        return fig        
# Run the app
#if __name__ == '__main__':
#    app.run_server()
