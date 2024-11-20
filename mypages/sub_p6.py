import pandas as pd
import plotly.express as px
import folium
import streamlit as st
from streamlit_folium import st_folium

def app():
    


    data = pd.read_csv("data/ladesaeulen.csv", delimiter=";")

    # Umbenennen Spalten: Breiten- und Längengrad
    data = data.rename(columns={"Längengrad": "lon", "Breitengrad": "lat"})

    st.subheader("Ladesäulen mit High Power Charging")
    
    # Filter: Daten nur für High Power Charging
    data = data[data['Ladegeschwindigkeit'] == 'High Power Charging']
    
    hpc_nach_jahr = data.groupby("Inbetriebnahmejahr").size().reset_index(name="Anzahl")

    st.write(hpc_nach_jahr)
    


    # Karte für Ladegeschwindigkeit
    st.subheader("Karte der Ladesäulen mit High Power Charging (ab 2023)")
    
    # Filter: Daten ab 2023
    data = data[data['Inbetriebnahmejahr'] >= 2023]

    
    # Erstellen der Karte für Ladegeschwindigkeit
    m_speed = folium.Map(
        location=[51.2978, 8.1661],  # Deutschland: Breitengrad und Längengrad
        zoom_start=8
    )

    # Punkte für Ladegeschwindigkeit
    for index, row in data.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=3,                
            color="blue", 
            fill=True, 
            fill_color="blue", 
            fill_opacity=0.5  
        ).add_to(m_speed)

    st_folium(m_speed, width=700, height=500)
