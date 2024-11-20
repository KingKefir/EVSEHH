import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

# Daten laden
data = pd.read_csv("data/ladesaeulen.csv", delimiter=";")

# Umbenennen Spalten: Breiten- und Längengrad
data = data.rename(columns={"Längengrad": "lon", "Breitengrad": "lat"})

# App-Definition
def app():
    st.title("Karte - Anzahl der Ladesäulen")
    st.subheader("Zeitliche Entwicklung")


    # Jahr Filter
    year_filter = st.slider(
        "Wählen Sie das Jahr:",
        min_value=int(data['Inbetriebnahmejahr'].min()),
        max_value=int(data['Inbetriebnahmejahr'].max()),
        value=int(data['Inbetriebnahmejahr'].min()),
        step=1
    )
    # Umbenennen Spalten: Breiten- und Längengrad



    # Filtern der Daten nach Jahr
    filtered_data = data[data['Inbetriebnahmejahr'] <= year_filter]
    map_data = filtered_data[['lat', 'lon']]

    # Erstellen der Karte
    m = folium.Map(
        location=[51.1657, 10.4515],  # Deutschland: Breitengrad und Längengrad
        zoom_start=6                  # Zoom-Stufe, um ganz Deutschland zu sehen
    )

    # Kleine Punkte für jede Ladestation hinzufügen
    for index, row in map_data.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=2,                
            color="red", 
            fill=True, 
            fill_color="red", 
            fill_opacity=0.5  
        ).add_to(m)

    st_folium(m, width=700, height=500)
    