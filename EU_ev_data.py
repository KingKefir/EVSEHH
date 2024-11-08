import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster

# CSV-Daten einlesen
data = pd.read_csv("combined_ev_data_23.csv", delimiter=";", decimal=".", header=0)
# Erstelle ein DataFrame aus den CSV-Daten
df = pd.DataFrame(data)

# Koordinaten für die Mittelpunkte der Länder (es werden vereinfacht die Hauptstädte genutzt)
country_coords = {
    "Belgium": [50.8503, 4.3517],
    "Czech Republic": [50.0755, 14.4378],
    "Denmark": [55.6761, 12.5683],
    "Germany": [52.5200, 13.4050],
    "France": [48.8566, 2.3522],
    "Luxembourg": [49.6117, 6.13],
    "Netherlands": [52.3676, 4.9041],
    "Austria": [48.2082, 16.3738],
    "Poland": [52.2298, 21.0118],
    "Switzerland": [46.8182, 8.2275]
}

# Streamlit App: Darstellung
st.title("E-Mobilität in Deutschland und den Nachbarländern (2023)")
st.subheader("Anteil E-Autos")

# Erstelle Karte mit Folium
m = folium.Map(location=[50, 10], zoom_start=4)  # Startposition in Europa

# MarkerCluster hinzufügen, um Markierungen zu gruppieren
marker_cluster = MarkerCluster().add_to(m)

# Füge für jedes Land einen Marker hinzu
for _, row in df.iterrows():
    country = row["country"]
    percentage_ev = row["percentage_ev"]
    coords = country_coords[country]
    
    # Marker-Farbe basierend auf dem Anteil der EVs
    color = "green" if percentage_ev > 5 else "orange" if percentage_ev > 2 else "red"
    
    # Füge Marker mit Popup hinzu
    folium.CircleMarker(
        location=coords,
        radius=10,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=f"{country}: {percentage_ev:.2f}% EVs"
    ).add_to(marker_cluster)

# Zeige die Karte in Streamlit an
st.write("Karte der EV-Verteilung in Europa 2023:")
st.components.v1.html(m._repr_html_(), height=500)

# Optional: Zeige eine Tabelle der Daten an
st.write("Daten der Länder:")
st.dataframe(df)