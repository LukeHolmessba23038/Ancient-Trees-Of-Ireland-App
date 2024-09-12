import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv('HeritageTreesOfIreland_transformed_updated.csv')

# Streamlit App Title
st.title("Interactive Tree Map of Ireland")

# Filter for County
counties = st.multiselect(
    "Filter by County:",
    options=df["County"].unique(),
    default=df["County"].unique()
)

# Filter for Broad Type
broad_types = st.multiselect(
    "Filter by Broad Type:",
    options=df["BroadType"].unique(),
    default=df["BroadType"].unique()
)

# Filter for Common Name
common_names = st.multiselect(
    "Filter by Common Name:",
    options=df["CommonName"].unique(),
    default=df["CommonName"].unique()
)

# Filter for Age Range
age_ranges = st.multiselect(
    "Filter by Age Range:",
    options=df["Age Range"].unique(),
    default=df["Age Range"].unique()
)

# Apply filters
filtered_df = df[
    (df["County"].isin(counties)) &
    (df["BroadType"].isin(broad_types)) &
    (df["CommonName"].isin(common_names)) &
    (df["Age Range"].isin(age_ranges))
]

# Create Plotly Map
fig = px.scatter_mapbox(
    filtered_df,
    lat="North",
    lon="East",
    color="BroadType",
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
    mapbox_style="carto-positron",
    zoom=7
)

# Display the map
st.plotly_chart(fig)
