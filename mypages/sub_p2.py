import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
import streamlit as st

def app():
    st.title("Erster Ansatz: Analyse mit SQL und Tableau")

    # Pfad zur PNG-Datei
    image_path = "data/ERD.png"

    # Bild anzeigen
    st.image(image_path, caption="ERD der Datenbank", use_column_width=True)