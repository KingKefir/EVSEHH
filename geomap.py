import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import json

# Load GeoJSON data
geojson_file = 'app_stromnetz_emobility_EPSG_4326.json'
with open(geojson_file) as f:
    geojson_data = json.load(f)

# Streamlit app
st.title("Optimized GeoJSON Map Display")
st.write("This map displays clustered data from the GeoJSON file.")

# Create map
m = folium.Map(location=[53.56222084047539, 10.005592885872836], zoom_start=12)

# Create a MarkerCluster
marker_cluster = MarkerCluster().add_to(m)

# Add points to cluster
for feature in geojson_data['features']:
    coordinates = feature['geometry']['coordinates']

    folium.Marker(location=[coordinates[1], coordinates[0]]).add_to(marker_cluster)

# Display map in Streamlit
st_folium(m, width=700, height=500)
