import streamlit as st
import pandas as pd
import folium
from folium import Choropleth
from streamlit_folium import st_folium
import json
from folium.plugins import GroupedLayerControl

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

    # Füge Choropleth hinzu für die Länderflächen, basierend auf dem Anteil E-Autos
    choropleth1 = Choropleth(
        geo_data=geojson_url,
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

    
    # Quickinfo 
    # geojson_layer = folium.GeoJson(
    #     geojson_url,
    #     tooltip=folium.GeoJsonTooltip(
    #         fields=["NAME"],  # Das Attribut, das den Ländernamen enthält
    #         aliases=["Country:"],  # Label für das Tooltip
    #         labels=True
    #     ),
    #     style_function=lambda feature: {
    #         'color': 'black',
    #         'weight': '1'
    #     }
    # )
    # geojson_layer.add_to(m)
    choropleth1.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['NAME'],
            aliases=['Land:'],
            labels=True,
            sticky=True,
            localize=True,
            toLocaleString=True,
            style=("background-color: white; color: black; font-weight: bold;"),
            tooltip_template="""<div>Land: {name}"""
        )
    )

    # Zeige die Karte in Streamlit an
    st.write("Prozentualer Anteil der E-Autos an der Gesamtzahl 2023:")
    # st.components.v1.html(m._repr_html_(), height=500)


    # 2. Karte
    # Erstelle Karte mit Folium
    m = folium.Map(location=[50, 10], zoom_start=4)


    # Füge Choropleth hinzu für die Länderflächen, basierend auf dem Anteil E-Autos
    choropleth2 = Choropleth(
        geo_data=geojson_url,
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
    # geojson_layer = folium.GeoJson(
    #     geojson_url,
    #     tooltip=folium.GeoJsonTooltip(
    #         fields=["NAME"],  # Das Attribut, das den Ländernamen enthält
    #         aliases=["Country:"],  # Label für das Tooltip
    #         labels=True
    #     ),
    #     style_function=lambda feature: {
    #         'color': 'black',
    #         'weight': '1'
    #     }
    # )
    # geojson_layer.add_to(m)

    choropleth2.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['NAME'],
            aliases=['Country:'],
            labels=True,
            sticky=True,
            localize=True,
            toLocaleString=True,
            style=("background-color: white; color: black; font-weight: bold;"),
            tooltip_template="""<div>Country: {name}"""
        )
    )

    # Zeige die Karte in Streamlit an
    # st.write("Anzahl der E_Autos pro Ladestation 2023:")
    # st.components.v1.html(m._repr_html_(), height=500)

    folium.LayerControl(collapsed=True, position='bottomleft').add_to(map)

    GroupedLayerControl(
    groups={'groups1': [choropleth1, choropleth2]},
    collapsed=False,
    position='bottomright'
    ).add_to(map)

    st_map = st_folium(map, width=900, height=650)

    # Optional: Zeige eine Tabelle der Daten an
    st.subheader("Daten: Deutschland mit Nachbarländern")
    st.write("Die Daten stammen vom statistischen Amt der EU [Eurostat](https://ec.europa.eu/eurostat/web/main/data/database)")
    st.dataframe(df)