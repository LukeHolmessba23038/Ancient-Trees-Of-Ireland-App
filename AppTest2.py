import streamlit as st
import pandas as pd
import plotly.express as px
from pyproj import Proj, transform

# Function to convert Irish Grid Reference to Latitude and Longitude
def grid_to_latlon(grid_reference):
    # Assuming grid_reference is in the Irish Grid (e.g., "O123456")
    # Extract easting and northing from the grid reference (you may need to adapt this based on the exact format of the grid reference)
    # For example: "O123456" would be parsed into some form of (easting, northing)
    
    # Setup the projection for Irish Grid (EPSG:29903) to WGS84 (lat/lon, EPSG:4326)
    irish_grid = Proj(init="epsg:29903")
    wgs84 = Proj(init="epsg:4326")
    
    # Example conversion: This would require parsing the grid reference properly
    # You need to convert the grid reference to a usable format of easting and northing
    # In this placeholder, the exact parsing is skipped. You should replace with actual logic.
    easting, northing = 123456, 234567  # Replace this with your own parsing logic
    
    # Convert to lat/lon
    lon, lat = transform(irish_grid, wgs84, easting, northing)
    return lat, lon

# Load preprocessed dataset (update path if necessary)
df = pd.read_csv('HeritageTreesOfIreland_transformed_updated.csv')

# Create latitude and longitude columns by converting the grid reference
df['Latitude'], df['Longitude'] = zip(*df['GridReference'].apply(grid_to_latlon))

# Build Streamlit app layout
st.title("Interactive Tree Map of Ireland")

# County Dropdown
selected_counties = st.multiselect(
    "Filter by County:",
    options=df['County'].unique(),
    default=df['County'].unique()
)

# Broad Type Dropdown
selected_broad_types = st.multiselect(
    "Filter by Broad Type:",
    options=df['BroadType'].unique(),
    default=df['BroadType'].unique()
)

# Common Name Dropdown
selected_common_names = st.multiselect(
    "Filter by Common Name:",
    options=df['CommonName'].unique(),
    default=df['CommonName'].unique()
)

# Age Range Dropdown
selected_age_ranges = st.multiselect(
    "Filter by Age Range:",
    options=df['Age Range'].unique(),
    default=df['Age Range'].unique()
)

# Filter DataFrame based on selections
filtered_df = df[
    (df['County'].isin(selected_counties)) &
    (df['BroadType'].isin(selected_broad_types)) &
    (df['CommonName'].isin(selected_common_names)) &
    (df['Age Range'].isin(selected_age_ranges))
]

# Debug: Check the number of points remaining after filtering
st.write(f"Number of points to plot: {filtered_df.shape[0]}")

# Debug: Show the filtered dataframe's latitude (North) and longitude (East)
st.write(filtered_df[['Latitude', 'Longitude']])

# Create the scatter map using Plotly with OpenStreetMap style
if filtered_df.shape[0] > 0:
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
        mapbox_style="open-street-map",  # Use OpenStreetMap style
        zoom=7
    )

    # Update map layout
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_center={"lat": 53.1424, "lon": -7.6921},  # Center on Ireland
        mapbox_zoom=10  # Adjusted zoom for better debugging
    )

    # Display the map in Streamlit
    st.plotly_chart(fig)
else:
    st.write("No data available for the selected filters.")
