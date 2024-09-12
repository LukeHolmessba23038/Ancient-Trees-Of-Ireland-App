import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset from GitHub
df = pd.read_csv('https://raw.githubusercontent.com/LukeHolmessba23038/Ancient-Trees-Of-Ireland-App/main/HeritageTreesOfIreland_corrected.csv')

# Remove rows with missing lat/lon before mapping
df = df.dropna(subset=['Latitude', 'Longitude'])

# Set page config for better presentation
st.set_page_config(page_title="Ireland's Heritage Trees", layout="wide")

# Create a sidebar for the filters
st.sidebar.header("Filter the Trees")
selected_counties = st.sidebar.multiselect(
    "Filter by County:",
    options=df['County'].unique(),
    default=df['County'].unique(),
    help="Select the counties to view trees from specific regions."
)

selected_broad_types = st.sidebar.multiselect(
    "Filter by Broad Type:",
    options=df['BroadType'].unique(),
    default=df['BroadType'].unique(),
    help="Choose the broad types of trees you are interested in."
)

selected_common_names = st.sidebar.multiselect(
    "Filter by Common Name:",
    options=df['CommonName'].unique(),
    default=df['CommonName'].unique(),
    help="Pick the specific tree species by common names."
)

selected_age_ranges = st.sidebar.multiselect(
    "Filter by Age Range:",
    options=df['Age Range'].unique(),
    default=df['Age Range'].unique(),
    help="Filter trees based on their age range."
)

# Filter DataFrame based on selections
filtered_df = df[
    (df['County'].isin(selected_counties)) &
    (df['BroadType'].isin(selected_broad_types)) &
    (df['CommonName'].isin(selected_common_names)) &
    (df['Age Range'].isin(selected_age_ranges))
]

# Main title and description
st.title("🌳 Interactive Heritage Tree Map of Ireland")
st.markdown("""
This interactive map allows you to explore the ancient and significant trees of Ireland. 
Use the filters on the left to narrow down your search by county, tree type, common name, and age range.
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
            "Condition of tree": True,
            "County": True
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
st.sidebar.write("🌍 Developed by [Your Name](https://yourportfolio.com)")

