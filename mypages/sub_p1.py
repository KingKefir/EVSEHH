import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
import streamlit as st

# Daten laden
data = pd.read_csv("data\\ladesaeulenregister.csv", delimiter=";", on_bad_lines="skip", low_memory=False)
# Unnötige Spalten entfernen
data = data.drop(columns=['Adresszusatz', 'Public Key1', 'Public Key2', 'Public Key3', 'Public Key4' ])
data = data.dropna(subset=['Inbetriebnahmedatum'])
data = data.dropna(subset=['Betreiber'])

def app():
    st.title("Überblick über die Daten")

    # Datenüberblick
    st.write("Die Quelle für den hier analysierten Datensatz findet man unter diesem [Link](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/E-Mobilitaet/Ladesaeulenkarte/start.html)")
    st.write('''
            Der Datensatz wird laufend aktualisiert. Hier wurde die Version vom 12.11.2024 verwendet.
             ''')

    st.divider()

    st.write(f"Der Datensatz besteht aus {data.shape[0]} Zeilen und {data.shape[1]} Spalten.")

    # Datenvorschau anzeigen
    with st.expander("Datenvorschau"):
        st.write("Hier sieht man die ersten 10 Zeilen des Datensatzes.")
        st.write(data.head(10))

    st.write(data.isna().sum())

