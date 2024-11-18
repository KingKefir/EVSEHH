import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
import streamlit as st

# Daten laden
data = pd.read_csv("data/ladesaeulenregister.csv", delimiter=";", on_bad_lines="skip")
# Unnötige Spalten entfernen
data = data.drop(columns=['Adresszusatz', 'Public Key1', 'Public Key2', 'Public Key3', 'Public Key4' ])
data = data.dropna(subset=['Inbetriebnahmedatum'])
data = data.dropna(subset=['Betreiber'])

def app():
    st.title("Erster Ansatz: Analyse mit SQL und Tableau")

    # Pfad zur PNG-Datei
    image_path = "data/ERD.png"

    # Bild anzeigen
    st.image(image_path, caption="ERD der Datenbank", use_column_width=True)