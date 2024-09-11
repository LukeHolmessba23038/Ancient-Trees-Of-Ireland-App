#!/usr/bin/env python
# coding: utf-8

# Python Libraries and Dataset Load
import pandas as pd
import plotly.express as px
import dash
from dash.dependencies import Input, Output
from dash import dcc, html
from flask import Flask
import os  

# Initialize the Flask app
server = Flask(__name__)

# Initialize the Dash app and associate it with the Flask app
app = dash.Dash(__name__, server=server, url_base_pathname='/')

# Load preprocessed dataset
df = pd.read_csv('HeritageTreesOfIreland_transformed_updated.csv')

# Build Dash app layout
app.layout = html.Div([
    html.H1("Interactive Tree Map of Ireland"),
    
    html.Label("Filter by County:"),
    dcc.Dropdown(id='county-dropdown', 
                 options=[{'label': county, 'value': county} for county in df['County'].unique() if county], 
                 value=[], multi=True, placeholder="Select counties"),
    
    html.Label("Filter by Broad Type:"),
    dcc.Dropdown(id='broad-type-dropdown', 
                 options=[{'label': broad, 'value': broad} for broad in df['BroadType'].unique()], 
                 value=[], multi=True, placeholder="Select broad types"),
    
    html.Label("Filter by Common Name:"),
    dcc.Dropdown(id='common-name-dropdown', 
                 options=[{'label': name, 'value': name} for name in df['CommonName'].unique()], 
                 value=[], multi=True, placeholder="Select common names"),
    
    html.Label("Filter by Age Range:"),
    dcc.Dropdown(id='age-range-dropdown', 
                 options=[{'label': age, 'value': age} for age in df['Age Range'].unique()], 
                 value=[], multi=True, placeholder="Select age ranges"),
    
    dcc.Graph(id='tree-map')  # Graph output for the map
])

# Map Update Callback
@app.callback(
    Output('tree-map', 'figure'),
    [Input('county-dropdown', 'value'),
     Input('broad-type-dropdown', 'value'),
     Input('common-name-dropdown', 'value'),
     Input('age-range-dropdown', 'value')]
)
def update_map(selected_counties, selected_broad_types, selected_common_names, selected_age_ranges):
    # Start with the full dataframe
    filtered_df = df.copy()

    # Apply filters based on inputs
    if selected_counties:
        filtered_df = filtered_df[filtered_df['County'].isin(selected_counties)]
    if selected_broad_types:
        filtered_df = filtered_df[filtered_df['BroadType'].isin(selected_broad_types)]
    if selected_common_names:
        filtered_df = filtered_df[filtered_df['CommonName'].isin(selected_common_names)]
    if selected_age_ranges:
        filtered_df = filtered_df[filtered_df['Age Range'].isin(selected_age_ranges)]

    # Create the scatter map using Plotly
    fig = px.scatter_mapbox(
        filtered_df, lat="Latitude", lon="Longitude", color="BroadType",
        hover_data={
            "CommonName": True,
            "TaxonName": True,
            "BroadType": True,
            "Age Range": True,
            "Tree form": True,
            "Condition of tree": True,
            "SiteName": True,
            "County": True
        },
        mapbox_style="carto-positron", zoom=7
    )

    # Update map layout
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_zoom=5,
        mapbox_center={"lat": 53.1424, "lon": -7.6921}  # Center on Ireland
    )

    return fig

# Define a basic Flask route for a homepage
@server.route('/')
def index():
    return "<h1>Welcome to the Interactive Trees of Ireland Dashboard!</h1>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8053))  # Use the port from the environment, default to 8053 if not available
    app.run_server(debug=False, port=port, host='0.0.0.0')  # Bind to 0.0.0.0 to accept all connections


