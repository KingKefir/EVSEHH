import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
import streamlit as st
import base64
from mypages import sub_p0, sub_p1, sub_p2,sub_p3, Page1, page3, page6, page7, page8

warnings.filterwarnings("ignore")

# Daten laden
# data = pd.read_csv("data\ladesaeulenregister.csv", delimiter=";", on_bad_lines="skip")
# # Unnötige Spalten entfernen
# data = data.drop(columns=['Adresszusatz', 'Public Key1', 'Public Key2', 'Public Key3', 'Public Key4' ])
# data = data.dropna(subset=['Inbetriebnahmedatum'])
# data = data.dropna(subset=['Betreiber'])

# 'Betreiber', 'Straße', 'Hausnummer', 'Adresszusatz', 'Postleitzahl','Ort', 'Bundesland', 'Kreis/kreisfreie Stadt', 'Breitengrad','Längengrad', 'Inbetriebnahmedatum','Nennleistung Ladeeinrichtung [kW]', 'Art der Ladeeinrichung','Anzahl Ladepunkte', 'Steckertypen1', 'P1 [kW]', 'Public Key1','Steckertypen2', 'P2 [kW]', 'Public Key2', 'Steckertypen3', 'P3 [kW]','Public Key3', 'Steckertypen4', 'P4 [kW]', 'Public Key4'],


# HTML für Titel mit Rahmen und anderer Schriftart
title_html = """
    <div style="
        border: 3px solid #000000;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        background-color: #dbe9f4;
        font-size: 24px;
        color: #000000;
        font-weight: bold;">
        LADEINFRASTRUKTUR IN DEUTSCHLAND
    </div>
"""

# Anzeige des Titels mit HTML und CSS
st.markdown(title_html, unsafe_allow_html=True)

pages = {
    "0. Startseite": sub_p0,
    "1. Überblick über die Daten": sub_p1,
    "2. Erster Ansatz: Analyse mit SQL und Tableau": sub_p2,
    "3. Analyse der Ladesäulen": sub_p3,
    "4. titel": Page1,
    "5. titel": page8
        }


st.sidebar.title("Navigation")
select = st.sidebar.radio("Gehe zu:", list(pages.keys()))
pages[select].app()