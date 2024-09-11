#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

# Python Libraries and Dataset Load
import pandas as pd
import plotly.express as px
import dash
from dash.dependencies import Input, Output
from dash import dcc, html
import re
from flask import Flask, render_template

# Initialize the Flask app
server = Flask(__name__)

# Initialize the Dash app and associate it with the Flask app
app = dash.Dash(__name__, server=server, url_base_pathname='/')

# Load the dataset with transformed coordinates
df = pd.read_csv('HeritageTreesOfIreland_transformed.csv')

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
    'Abies bracteata': 'Bristlecone Fir',
    'Abies nordmanniana': 'Nordmann Fir',
    'Abies procera': 'Noble Fir',
    'Acacia dealbata': 'Silver Wattle',
    'Acer campestre': 'Field Maple',
    'Acer cappadocicum': 'Cappadocian Maple',
    'Acer macrophyllum': 'Bigleaf Maple',
    'Acer opalus': 'Italian Maple',
    'Acer platanoides': 'Norway Maple',
    'Acer pseudoplatanus': 'Sycamore Maple',
    'Acer rubrum': 'Red Maple',
    'Acer saccharinum': 'Silver Maple',
    'Aesculus hippocastanum': 'Horse Chestnut',
    'Aesculus x carnea': 'Red Horse Chestnut',
    'Ailanthus altissima': 'Tree of Heaven',
    'Alnus glutinosa': 'Common Alder',
    'Araucaria araucana': 'Monkey Puzzle Tree',
    'Araucaria heterophylla': 'Norfolk Island Pine',
    'Arbutus unedo': 'Strawberry Tree',
    'Arbutus unedo x andrachne = A. x andrachnoides': 'Hybrid Strawberry Tree',
    'Betula pendula': 'Silver Birch',
    'Buxus sempervirens': 'Common Box',
    'Calocedrus decurrens': 'Incense Cedar',
    'Carpinus betulus': 'European Hornbeam',
    'Castanea sativa': 'Sweet Chestnut',
    'Catalpa bignonioides': 'Southern Catalpa',
    'Catalpa x erubescens': 'Hybrid Catalpa',
    'Cedrus atlantica': 'Atlas Cedar',
    'Cedrus deodara': 'Deodar Cedar',
    'Cedrus libani': 'Cedar of Lebanon',
    'Cercidiphyllum japonicum': 'Katsura Tree',
    'Chamaecyparis lawsoniana': 'Lawson Cypress',
    'Cinnamomum camphora': 'Camphor Tree',
    'Clethra arborea': 'Lily of the Valley Tree',
    'Cordyline australis': 'Cabbage Tree',
    'Corylus avellana': 'Common Hazel',
    'Crataegus monogyna': 'Common Hawthorn',
    'Cryptomeria japonica': 'Japanese Cedar',
    'Cupressus cashmeriana': 'Kashmir Cypress',
    'Cupressus lusitanica': 'Mexican Cypress',
    'Cupressus macrocarpa': 'Monterey Cypress',
    'Cupressus sempervirens': 'Italian Cypress',
    'Cyathea dealbata': 'Silver Fern',
    'Dicksonia antarctica': 'Tasmanian Tree Fern',
    'Eucalyptus globulus': 'Tasmanian Blue Gum',
    'Eucalyptus johnstonii': 'Johnston’s Gum',
    'Eucryphia x nymansensis': 'Nymans Eucryphia',
    'Euonymus europaeus': 'European Spindle',
    'Fagus sylvatica': 'European Beech',
    'Fraxinus excelsior': 'European Ash',
    'Ginkgo biloba': 'Ginkgo',
    'Griselinia littoralis': 'Broadleaf Griselinia',
    'Ilex aquifolium': 'Common Holly',
    'Ilex aquifolium x perado = I. x altaclerensis': 'Altaclera Holly',
    'Jubaea chilensis': 'Chilean Wine Palm',
    'Juglans ailanthifolia': 'Japanese Walnut',
    'Juglans nigra': 'Black Walnut',
    'Juglans regia': 'English Walnut',
    'Juniperus communis': 'Common Juniper',
    'Laburnum alpinum': 'Alpine Laburnum',
    'Larix decidua': 'European Larch',
    'Laureliopsis philippiana': 'Chilean Laurel',
    'Laurus nobilis': 'Bay Laurel',
    'Ligustrum lucidum': 'Glossy Privet',
    'Liquidambar styraciflua': 'Sweetgum',
    'Liriodendron tulipifera': 'Tulip Tree',
    'Luma apiculata': 'Chilean Myrtle',
    'Magnolia acuminata': 'Cucumber Tree',
    'Magnolia campbellii': 'Campbell’s Magnolia',
    'Magnolia delavayi': 'Delavay Magnolia',
    'Magnolia grandiflora': 'Southern Magnolia',
    'Magnolia sargentiana': 'Sargent’s Magnolia',
    'Malus sylvestris': 'European Crab Apple',
    'Metasequoia glyptostroboides': 'Dawn Redwood',
    'Metrosideros excelsa': 'New Zealand Christmas Tree',
    'Michelia doltsopa': 'Michelia',
    'Morus alba': 'White Mulberry',
    'Morus nigra': 'Black Mulberry',
    'Nothofagus alpina': 'Rauli Beech',
    'Nothofagus betuloides': 'Magellan’s Beech',
    'Nothofagus cunninghamii': 'Myrtle Beech',
    'Nothofagus dombeyi': 'Dombey’s Southern Beech',
    'Olea europaea': 'Olive Tree',
    'Paulownia tomentosa': 'Empress Tree',
    'Phoenix canariensis': 'Canary Island Date Palm',
    'Photinia serrulata': 'Chinese Photinia',
    'Phyllocladus trichomanoides': 'Tanekaha',
    'Picea abies': 'Norway Spruce',
    'Picea breweriana': 'Brewer’s Spruce',
    'Picea sitchensis': 'Sitka Spruce',
    'Pinus cembra': 'Swiss Pine',
    'Pinus montezumae': 'Montezuma Pine',
    'Pinus pinaster': 'Maritime Pine',
    'Pinus pinea': 'Stone Pine',
    'Pinus radiata': 'Monterey Pine',
    'Pinus sylvestris': 'Scots Pine',
    'Platanus orientalis': 'Oriental Plane',
    'Platanus occidentalis x orientalis = P. x hispanica': 'London Plane',
    'Podocarpus salignus': 'Willow-leaf Podocarp',
    'Populus nigra': 'Black Poplar',
    'Populus nigra x deltoides = P. x canadensis': 'Hybrid Black Poplar',
    'Populus alba x tremula = P. x canescens': 'Grey Poplar',
    'Populus x vernirubens': 'Hybrid Poplar',
    'Prunus avium': 'Wild Cherry',
    'Prunus laurocerasus': 'Cherry Laurel',
    'Prunus spinosa': 'Blackthorn',
    'Pseudotsuga menziesii': 'Douglas Fir',
    'Pterocarya fraxinifolia': 'Caucasian Wingnut',
    'Pyrus communis': 'Common Pear',
    'Quercus castaneifolia': 'Chestnut-leaved Oak',
    'Quercus cerris': 'Turkey Oak',
    'Quercus ilex': 'Holm Oak',
    'Quercus petraea': 'Sessile Oak',
    'Quercus robur': 'English Oak',
    'Quercus suber': 'Cork Oak',
    'Rhododendron arboreum': 'Tree Rhododendron',
    'Robinia pseudoacacia': 'Black Locust',
    'Salix alba': 'White Willow',
    'Salix alba x babylonica = S. x sepulcralis': 'Weeping Willow',
    'Sambucus nigra': 'Elder',
    'Sequoia sempervirens': 'Coast Redwood',
    'Sequoiadendron giganteum': 'Giant Sequoia',
    'Sophora japonica': 'Japanese Pagoda Tree',
    'Sorbus aria': 'Whitebeam',
    'Sorbus aucuparia': 'Rowan',
    'Sorbus devoniensis': 'Devon Whitebeam',
    'Sorbus x latifolia': 'Broad-leaved Whitebeam',
    'Sorbus aucuparia x aria = S. x thuringiaca': 'Hybrid Rowan',
    'Taxodium distichum': 'Bald Cypress',
    'Taxus baccata': 'English Yew',
    'Tetradium daniellii': 'Bee-bee Tree',
    'Thuja plicata': 'Western Red Cedar',
    'Tilia platyphyllos': 'Large-leaved Lime',
    'Tilia tomentosa': 'Silver Lime',
    'Tilia platyphyllos x cordata = T. x europaea': 'Common Lime',
    'Toona sinensis': 'Chinese Cedar',
    'Trochodendron aralioides': 'Wheel Tree',
    'Tsuga heterophylla': 'Western Hemlock',
    'Ulmus glabra': 'Wych Elm',
    'Ulmus laevis': 'European White Elm',
    'Ulmus minor': 'Field Elm',
    'Zelkova carpinifolia': 'Caucasian Zelkova'
} 

scientific_to_type = {
    'Abies alba': 'Firs',
    'Abies bracteata': 'Firs',
    'Abies nordmanniana': 'Firs',
    'Abies procera': 'Firs',
    'Acacia dealbata': 'Acacias',
    'Acer campestre': 'Maples',
    'Acer cappadocicum': 'Maples',
    'Acer macrophyllum': 'Maples',
    'Acer opalus': 'Maples',
    'Acer platanoides': 'Maples',
    'Acer pseudoplatanus': 'Maples',
    'Acer rubrum': 'Maples',
    'Acer saccharinum': 'Maples',
    'Aesculus hippocastanum': 'Horse Chestnuts',
    'Aesculus x carnea': 'Horse Chestnuts',
    'Ailanthus altissima': 'Tree of Heaven',
    'Alnus glutinosa': 'Alders',
    'Araucaria araucana': 'Monkey Puzzle',
    'Araucaria heterophylla': 'Norfolk Island Pines',
    'Arbutus unedo': 'Strawberry Trees',
    'Arbutus unedo x andrachne = A. x andrachnoides': 'Strawberry Trees',
    'Betula pendula': 'Birches',
    'Buxus sempervirens': 'Boxwoods',
    'Calocedrus decurrens': 'Incense Cedars',
    'Carpinus betulus': 'Hornbeams',
    'Castanea sativa': 'Chestnuts',
    'Catalpa bignonioides': 'Catalpas',
    'Catalpa x erubescens': 'Catalpas',
    'Cedrus atlantica': 'Cedars',
    'Cedrus deodara': 'Cedars',
    'Cedrus libani': 'Cedars',
    'Cercidiphyllum japonicum': 'Katsura Trees',
    'Chamaecyparis lawsoniana': 'False Cypresses',
    'Cinnamomum camphora': 'Camphor Trees',
    'Clethra arborea': 'Clethra',
    'Cordyline australis': 'Cabbage Trees',
    'Corylus avellana': 'Hazels',
    'Crataegus monogyna': 'Hawthorns',
    'Cryptomeria japonica': 'Japanese Cedars',
    'Cupressus cashmeriana': 'Cypresses',
    'Cupressus lusitanica': 'Cypresses',
    'Cupressus macrocarpa': 'Monterey Cypresses',
    'Cupressus sempervirens': 'Italian Cypresses',
    'Cyathea dealbata': 'Tree Ferns',
    'Dicksonia antarctica': 'Tree Ferns',
    'Eucalyptus globulus': 'Eucalypts',
    'Eucalyptus johnstonii': 'Eucalypts',
    'Eucryphia x nymansensis': 'Eucryphias',
    'Euonymus europaeus': 'Spindle Trees',
    'Fagus sylvatica': 'Beeches',
    'Fraxinus excelsior': 'Ashes',
    'Ginkgo biloba': 'Ginkgo',
    'Griselinia littoralis': 'Griselinias',
    'Ilex aquifolium': 'Hollies',
    'Ilex aquifolium x perado = I. x altaclerensis': 'Hollies',
    'Jubaea chilensis': 'Chilean Wine Palm',
    'Juglans ailanthifolia': 'Walnuts',
    'Juglans nigra': 'Walnuts',
    'Juglans regia': 'Walnuts',
    'Juniperus communis': 'Junipers',
    'Laburnum alpinum': 'Laburnums',
    'Larix decidua': 'Larches',
    'Laureliopsis philippiana': 'Laureliopsis',
    'Laurus nobilis': 'Laurels',
    'Ligustrum lucidum': 'Privets',
    'Liquidambar styraciflua': 'Sweetgums',
    'Liriodendron tulipifera': 'Tulip Trees',
    'Luma apiculata': 'Luma',
    'Magnolia acuminata': 'Magnolias',
    'Magnolia campbellii': 'Magnolias',
    'Magnolia delavayi': 'Magnolias',
    'Magnolia grandiflora': 'Magnolias',
    'Magnolia sargentiana': 'Magnolias',
    'Malus sylvestris': 'Crabapples',
    'Metasequoia glyptostroboides': 'Dawn Redwoods',
    'Metrosideros excelsa': 'Pohutukawa',
    'Michelia doltsopa': 'Michelia',
    'Morus alba': 'Mulberries',
    'Morus nigra': 'Mulberries',
    'Nothofagus alpina': 'Southern Beeches',
    'Nothofagus betuloides': 'Southern Beeches',
    'Nothofagus cunninghamii': 'Southern Beeches',
    'Nothofagus dombeyi': 'Southern Beeches',
    'Olea europaea': 'Olives',
    'Paulownia tomentosa': 'Empress Trees',
    'Phoenix canariensis': 'Canary Island Palms',
    'Photinia serrulata': 'Photinia',
    'Phyllocladus trichomanoides': 'Celery Pines',
    'Picea abies': 'Spruces',
    'Picea breweriana': 'Spruces',
    'Picea sitchensis': 'Spruces',
    'Pinus cembra': 'Pines',
    'Pinus montezumae': 'Pines',
    'Pinus pinaster': 'Pines',
    'Pinus pinea': 'Pines',
    'Pinus radiata': 'Pines',
    'Pinus sylvestris': 'Pines',
    'Platanus orientalis': 'Plane Trees',
    'Platanus occidentalis x orientalis = P. x hispanica': 'Plane Trees',
    'Podocarpus salignus': 'Podocarps',
    'Populus nigra': 'Poplars',
    'Populus nigra x deltoides = P. x canadensis': 'Poplars',
    'Populus alba x tremula = P. x canescens': 'Poplars',
    'Populus x vernirubens': 'Poplars',
    'Prunus avium': 'Cherries'   
}

# Apply mappings
df['CommonName'] = df['TaxonName'].map(scientific_to_common)
df['BroadType'] = df['TaxonName'].map(scientific_to_type)

# Fill missing values with the scientific name if no common name is found
df['CommonName'].fillna(df['TaxonName'], inplace=True)
df['BroadType'].fillna('Other', inplace=True)

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
    app.run_server(debug=True, port=8054)



# In[ ]:





# In[ ]:




