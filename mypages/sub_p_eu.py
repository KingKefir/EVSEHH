import streamlit as st
import pandas as pd
import folium
from folium import Choropleth
from streamlit_folium import st_folium
import json
import requests
from folium.plugins import GroupedLayerControl

def create_tooltip():
    return folium.features.GeoJsonTooltip(
           fields=['NAME', 'total_number_cars', 'number_ev', 'percentage_ev', 'ev_per_evse'],
            aliases=['Country:', 'Fahzeuge Gesamt:', 'EVs Gesamt:', 'Anteil EV(%): ', 'EV pro Ladesäulen'],
            labels=True,
            sticky=True,
            localize=True,
            toLocaleString=True,
            style=("background-color: white; color: black; font-weight: bold;"),
            tooltip_template="""<div>Country: {name}<br>Fahrzeuge Gesamt: {total_number_cars}<br>EV Gesamt: {number_ev}<br>Anteil EV(%): {percentage_ev}<br>EV pro Ladesäulen: {ev_per_evse}</div>"""
    )

def app():
       # CSV-Daten einlesen
    data = pd.read_csv("data/combined_ev_data_23.csv", delimiter=";", decimal=".", header=0)
    df = pd.DataFrame(data)

    # Streamlit App: Darstellung
    st.title("Einordnung: Deutschland und seine Nachbarländer (2023)")
    st.subheader("Anteil E-Autos an Gesamtzahl Autos")

    # 1. Karte
    # Erstelle Karte mit Folium
    map = folium.Map(location=[50, 10], zoom_start=5, scrollWheelZoom=False, tiles='CartoDB positron')

    # Lade eine GeoJSON-Datei mit Ländergrenzen
    geojson_url = "https://raw.githubusercontent.com/leakyMirror/map-of-europe/master/GeoJSON/europe.geojson"
    res = requests.get(geojson_url)
    geodata = res.json()
    
    for feature in geodata['features']:
        name = feature['properties']['NAME']
        total_number_cars = df.loc[df['country'] == name, 'total_number_cars']
        number_ev = df.loc[df['country'] == name, 'number_ev']
        percentage_ev =  df.loc[df['country'] == name, 'percentage_ev']
        ev_per_evse =  df.loc[df['country'] == name, 'number_ev_per_charging_point']

        feature['properties']['total_number_cars'] = int(total_number_cars.iloc[0]) if not total_number_cars.empty else 0
        feature['properties']['number_ev'] = int(number_ev.iloc[0]) if not number_ev.empty else 0
        feature['properties']['percentage_ev'] = round(float(percentage_ev.iloc[0]), 2) if not percentage_ev.empty else 0
        feature['properties']['ev_per_evse'] = int(ev_per_evse.iloc[0]) if not ev_per_evse.empty else 0

    # Füge Choropleth hinzu für die Länderflächen, basierend auf dem Anteil E-Autos
    choropleth1 = Choropleth(
        geo_data=geodata,
        name="Anteil E-Autos (%)",
        data=df,
        columns=["country", "percentage_ev"],
        key_on="feature.properties.NAME",  # Der Name des Landes in der GeoJSON-Datei
        fill_color="Greens",  # Farbpalette
        fill_opacity=0.7,
        line_opacity=0.5,
        overlay=True,
        control=True,
        show=True,
        legend_name="Anteil E-Autos (%)",
        threshold_scale=[0, 2, 5, 10, 15]
    ).add_to(map)

    choropleth1.geojson.add_child(create_tooltip())

    # Zeige die Karte in Streamlit an
    st.write("Prozentualer Anteil der E-Autos an der Gesamtzahl 2023:")


    # Füge Choropleth hinzu für die Länderflächen, basierend auf dem Anteil E-Autos
    choropleth2 = Choropleth(
        geo_data=geodata,
        name="Durchschnittliche Anzahl E-Autos pro Ladepunkt",
        data=df,
        columns=["country", "number_ev_per_charging_point"],
        key_on="feature.properties.NAME",  # Der Name des Landes in der GeoJSON-Datei
        fill_color="Blues_r",  # Farbpalette
        fill_opacity=0.7,
        line_opacity=0.5,
        overlay=True,
        control=True,
        show=False,
        legend_name="Durchschnittliche Anzahl E-Autos pro Ladepunkt",
        threshold_scale=[0, 5, 10, 15, 20, 25]
    ).add_to(map)

    # Quickinfo 

    choropleth2.geojson.add_child(create_tooltip())

    folium.LayerControl(collapsed=True, position='bottomleft').add_to(map)

    GroupedLayerControl(
    groups={'EU': [choropleth1, choropleth2]},
    collapsed=False,
    position='bottomright'
    ).add_to(map)

    st_map = st_folium(map, width=900, height=650)

    # Optional: Zeige eine Tabelle der Daten an
    st.subheader("Daten: Deutschland mit Nachbarländern")
    st.write("Die Daten stammen vom statistischen Amt der EU [Eurostat](https://ec.europa.eu/eurostat/web/main/data/database)")
    st.dataframe(df)