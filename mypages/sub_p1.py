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
    st.title("Überblick über die Daten")

    # Datenüberblick
    st.write("Die verwendeten Daten stammen von der Bundesnetzagentur. Man findet sie unter diesem [Link](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/E-Mobilitaet/Ladesaeulenkarte/start.html).")
    st.write(f"Der Datensatz besteht aus {data.shape[0]} Zeilen und {data.shape[1]} Spalten.")
    st.write("Die Daten werden laufend aktualisiert. Hier wurde die Version vom 12.11.2024 verwendet.")
    
    st.divider()
    st.write("**Dies sind alle vorkommenden Spaltenbezeichnungen:**")
    col_names = data.columns.tolist()
    for col_name in col_names:
        st.write("-",col_name)

    st.divider()

    # Datenvorschau 
    with st.expander("Datenvorschau"):
        st.write("Hier sieht man die ersten 10 Zeilen des Datensatzes.")
        st.write(data.head(10))

    st.write("**Datenüberblick mit Spaltenauswahl**")

    cols = st.multiselect("Spaltenauswahl:",data.columns.tolist(), default = ["Betreiber", "Bundesland", "Inbetriebnahmedatum"])
    st.dataframe(data[cols])
    


