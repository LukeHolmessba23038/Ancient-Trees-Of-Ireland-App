#!/usr/bin/env python
# coding: utf-8

# Python Libraries and Dataset Load
import pandas as pd
import plotly.express as px
import dash
from dash.dependencies import Input, Output
from dash import dcc, html, Input, Output
import re
from pyproj import Transformer
from flask import Flask, render_template

# Initialize the Flask app
server = Flask(__name__)

# Initialize the Dash app and associate it with the Flask app
app = dash.Dash(__name__, server=server, url_base_pathname='/')

# Load dataset
df = pd.read_csv('HeritageTreesOfIreland.csv')

# Preprocessing
df['StartDate'] = pd.to_datetime(df['StartDate'], dayfirst=True, errors='coerce')
df['EndDate'] = pd.to_datetime(df['EndDate'], dayfirst=True, errors='coerce')
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

# Extract county from 'SiteName' after "Co."
df['County'] = df['SiteName'].str.extract(r'Co\.\s*(\w+)')

# Remove rows where 'County' is None or null
df = df.dropna(subset=['County'])

# Dictionary mappings for common names and tree types
scientific_to_common = {
    'Abies alba': 'European Silver Fir',
    # (Other mappings...)
}

scientific_to_type = {
    'Abies alba': 'Firs',
    # (Other mappings...)
}

# Apply mappings
df['CommonName'] = df['TaxonName'].map(scientific_to_common)
df['BroadType'] = df['TaxonName'].map(scientific_to_type)

# Fill missing values with the scientific name if no common name is found
df['CommonName'].fillna(df['TaxonName'], inplace=True)
df['BroadType'].fillna('Other', inplace=True)

# Convert Irish Grid (EPSG:29903) coordinates to WGS84 (EPSG:4326)
transformer = Transformer.from_crs("EPSG:29903", "EPSG:4326", always_xy=True)
df['Longitude'], df['Latitude'] = transformer.transform(df['East'].values, df['North'].values)

# Check conversion
print(df[['East', 'North', 'Latitude', 'Longitude']].head())

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

# Running the app (for standalone use)
if __name__ == '__main__':
    app.run_server(debug=True, port=8053)
