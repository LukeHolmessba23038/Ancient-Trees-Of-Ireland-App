import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset from GitHub
df = pd.read_csv('https://raw.githubusercontent.com/LukeHolmessba23038/Ancient-Trees-Of-Ireland-App/main/HeritageTreesOfIreland_corrected.csv')

# Remove rows with missing lat/lon before mapping
df = df.dropna(subset=['Latitude', 'Longitude'])

# Filter out trees with coordinates outside Ireland's geographical boundaries
# Approximate bounds: Latitude between 51.4 and 55.5, Longitude between -10.5 and -5.5
df = df[(df['Latitude'] >= 51.4) & (df['Latitude'] <= 55.5) & (df['Longitude'] >= -10.5) & (df['Longitude'] <= -5.5)]

# Set page config for better presentation
st.set_page_config(page_title="Ireland's Heritage Trees", layout="wide")

# Create a sidebar for the filters
st.sidebar.header("Filter the Trees")

# Dropdown for Broad Type
selected_broad_type = st.sidebar.selectbox(
    "Filter by Broad Type:",
    options=['All'] + list(df['BroadType'].unique()),
    index=0,
    help="Choose the broad type of trees you are interested in."
)

# Dropdown for Common Name
selected_common_name = st.sidebar.selectbox(
    "Filter by Common Name:",
    options=['All'] + list(df['CommonName'].unique()),
    index=0,
    help="Pick the specific tree species by common names."
)

# Dropdown for Age Range
selected_age_range = st.sidebar.selectbox(
    "Filter by Age Range:",
    options=['All'] + list(df['Age Range'].unique()),
    index=0,
    help="Filter trees based on their age range."
)

# Filter DataFrame based on selections
filtered_df = df.copy()

if selected_broad_type != 'All':
    filtered_df = filtered_df[filtered_df['BroadType'] == selected_broad_type]

if selected_common_name != 'All':
    filtered_df = filtered_df[filtered_df['CommonName'] == selected_common_name]

if selected_age_range != 'All':
    filtered_df = filtered_df[filtered_df['Age Range'] == selected_age_range]

# Main title and description
st.title("🌳 Interactive Heritage Tree Map of Ireland")
st.markdown("""
This interactive map allows you to explore the ancient and significant trees of Ireland. 
Use the filters on the left to narrow down your search by tree type, common name, and age range.
""")

# Display a count of how many trees are shown
st.write(f"Displaying **{filtered_df.shape[0]}** heritage trees based on your filters.")

# Map display section
if filtered_df.shape[0] > 0:
    fig = px.scatter_mapbox(
        filtered_df, lat="Latitude", lon="Longitude", color="BroadType",
        hover_data={
            "CommonName": True,
            "TaxonName": True,
            "BroadType": True,
            "Age Range": True,
            "Tree form": True,
            "Condition of tree": True
        },
        mapbox_style="carto-positron",  # Light, modern map style
        zoom=7
    )

    # Update map layout
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_center={"lat": 53.1424, "lon": -7.6921},  # Center on Ireland
        mapbox_zoom=7  # Adjusted zoom for better view
    )

    # Display the map
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for the selected filters. Try changing your selection.")

# Footer information
st.sidebar.markdown("---")
st.sidebar.write("🌍 Developed by Luke Holmes")
