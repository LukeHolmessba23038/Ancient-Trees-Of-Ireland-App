import streamlit as st
import pandas as pd
import plotly.express as px

# Load preprocessed dataset with latitude and longitude (update path if necessary)
df = pd.read_csv('HeritageTreesOfIreland_with_latlon.csv')

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
            "County": True
        },
        mapbox_style="open-street-map",  # Use OpenStreetMap style
        zoom=7
    )

    # Update map layout
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_center={"lat": 53.1424, "lon": -7.6921},  # Center on Ireland
        mapbox_zoom=7  # Adjusted zoom for better view
    )

    # Display the map in Streamlit
    st.plotly_chart(fig)
else:
    st.write("No data available for the selected filters.")
