import streamlit as st
import pandas as pd
import plotly.express as px

# Function to manually convert grid references to latitude and longitude
def grid_to_latlon(grid_reference):
    """
    A simple manual conversion for the Irish Grid reference to latitude and longitude.
    This is an approximation. You'll need to adapt it to your exact grid reference format.
    """

    grid_letters = {
        'A': (0, 0), 'B': (100000, 0), 'C': (200000, 0), 'D': (300000, 0),
        'E': (400000, 0), 'F': (0, 100000), 'G': (100000, 100000), 'H': (200000, 100000),
        'J': (300000, 100000), 'K': (400000, 100000), 'L': (0, 200000), 'M': (100000, 200000),
        'N': (200000, 200000), 'O': (300000, 200000), 'Q': (400000, 200000)
    }

    # Parse the grid reference (e.g., "O123456")
    if len(grid_reference) < 2:
        return None, None  # Invalid format

    # Extract the grid letter and the numerical part
    grid_letter = grid_reference[0].upper()
    numbers = grid_reference[1:]

    # Split the numbers into easting and northing (assumes equal parts, 6 digits total)
    if len(numbers) == 6:
        easting = int(numbers[:3]) * 100  # Convert to full easting
        northing = int(numbers[3:]) * 100  # Convert to full northing
    else:
        return None, None  # Invalid format

    # Adjust based on grid letter
    if grid_letter in grid_letters:
        grid_offset_easting, grid_offset_northing = grid_letters[grid_letter]
        easting += grid_offset_easting
        northing += grid_offset_northing
    else:
        return None, None  # Invalid grid letter

    # Convert the easting/northing into latitude and longitude (this is a basic approximation)
    # You may want to use a more precise conversion depending on the system you're working with.
    lat = northing / 1000000 * 54  # Rough approximation for Ireland
    lon = easting / 1000000 * -8   # Rough approximation for Ireland

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

# Debug: Show the filtered dataframe's latitude and longitude
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
