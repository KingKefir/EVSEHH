import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

# Daten laden
data = pd.read_csv("ladesaeulenregister.csv", delimiter=";", on_bad_lines="skip")

# Unnötige Spalten / Zeilen entfernen
data = data.drop(columns=['Adresszusatz', 'Public Key1', 'Public Key2', 'Public Key3', 'Public Key4'])
data = data.dropna(subset=['Inbetriebnahmedatum', 'Betreiber', 'Bundesland'])

data['Breitengrad'] = data['Breitengrad'].str.replace(',', '.').str.rstrip('.').astype(float)
data['Längengrad'] = data['Längengrad'].str.replace(',', '.').str.rstrip('.').astype(float)

data = data.rename(columns={'Breitengrad': 'lat', 'Längengrad': 'lon'})

# Jahr der Inbetriebnahme in neue Spalte
data['Inbetriebnahmejahr'] = pd.to_datetime(data['Inbetriebnahmedatum'], format='%d.%m.%Y', errors='coerce').dt.year

# App-Definition
def app():
    st.title("Karte - Anzahl der Ladesäulen nach Jahren")


    # Jahr Filter
    year_filter = st.slider(
        "Wählen Sie das Jahr:",
        min_value=int(data['Inbetriebnahmejahr'].min()),
        max_value=int(data['Inbetriebnahmejahr'].max()),
        value=int(data['Inbetriebnahmejahr'].min()),
        step=1
    )

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
    