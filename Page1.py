import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json

APP_TITLE = 'Fraud and Identity Theft Report'
APP_SUB_TITLE = 'Source: Federal Trade Commission'


# TODO Filter Anzahl Säulen gesamt/per 100k/per EV je Bundesland
# def display_time_filters(df):
#     year_list = list(df['Year'].unique())
#     year_list.sort()
#     year = st.sidebar.selectbox('Year', year_list, len(year_list)-1)
#     st.header(f'{year}')
#     return year, quarter

# Load your data
file_path = 'data\ladesaeulenregister_Bundesnetzagentur_2024.csv'  # Replace with your CSV file path
data = pd.read_csv(file_path, sep=';', skiprows=10, low_memory=False)

bundesland_counts = data['Bundesland'].value_counts()

bundesland_counts = data['Bundesland'].value_counts().reset_index()
bundesland_counts.columns = ['Bundesland', 'Count']

# TODO Datensatz für KFZ einfügen

map = folium.Map(location=[51, 10.5], zoom_start=6, scrollWheelZoom=False, tiles='CartoDB positron')



with open('data\DE_niedrig.geo.json', encoding='utf-8') as f:
    geodata = json.load(f)


# Anzahl der Ladesäulen zum Geo-Datensatz hinzugefügt, um diesen im Landkarten-Tooltip anzeigbar zu machen
# TODO Anzahl der Ladensäulen pro 100k Einwohner berechnen und dem Tooltip hunzufügen
# TODO Anzahl der Ladensäulen pro 1000 EVs berechnen und dem Tooltip hunzufügen

# TODO folium.Layercontrol hinzufügen, wenn möglich


for feature in geodata['features']:
    bundesland = feature['properties']['name']
    count = bundesland_counts.loc[bundesland_counts['Bundesland'] == bundesland, 'Count']
    feature['properties']['Count'] = int(count) if not count.empty else 0


choropleth = folium.Choropleth(
    geo_data=geodata,
    name="Choropleth",
    data=bundesland_counts,
    columns=['Bundesland', 'Count'],
    key_on='feature.properties.name',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    overlay=True,
    control=True,
    legend_name="Ladesäulen per Bundesland"
).add_to(map)

# Add tooltip
choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(
        fields=['name', 'Count'],
        aliases=['Bundesland:', 'Anzahl Ladesäulen:'],
        labels=True,
        sticky=False,
        localize=True,
        toLocaleString=True,
        style=("background-color: white; color: black; font-weight: bold;"),
        tooltip_template="""<div>Bundesland: {name}<br>Count: {Count}</div>"""
    )
)


st_map = st_folium(map, width=700, height=650)