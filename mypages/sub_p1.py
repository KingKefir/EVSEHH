import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
import streamlit as st

# Daten laden
data_org = pd.read_csv("data/ladesaeulenregister.csv", delimiter=";", on_bad_lines="skip")
# Unnötige Spalten entfernen

data = pd.read_csv("data/ladesaeulen.csv", delimiter=";")

def app():
    st.title("Überblick über die Daten")
    st.subheader("Die Datenquelle")

    # Datenüberblick
    st.write("Die verwendeten Daten stammen von der Bundesnetzagentur. Man findet sie unter diesem [Link](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/E-Mobilitaet/Ladesaeulenkarte/start.html).")
    st.write(f"Der Datensatz besteht aus {data.shape[0]} Zeilen und {data.shape[1]} Spalten.")
    st.write("Die Daten werden laufend aktualisiert. Hier wurde die Version vom 12.11.2024 verwendet.")

    # Datenvorschau 
    with st.expander("Datenvorschau Originaldaten"):
        st.write("Hier sieht man die ersten 10 Zeilen des Datensatzes.")
        st.write(data.head(10))
    
    st.divider()
    st.write("**Dies sind alle vorkommenden Spaltenbezeichnungen - also die Informationen, die für jede öffentliche Ladesäule verfügbar sind:**")
    col_names = data_org.columns.tolist()
    for col_name in col_names:
        st.write("-",col_name)

    st.divider()

    st.subheader("Anpassung des Datensatzes - Erstellung von zwei neuen csv-Dateien (data/ladesaeulen.csv und ladeplaetze.csv) zur Vermeidung hoher Ladezeiten")
    st.markdown('''
                Folgende Anpassungen wurden durchgeführt:
                - Entfernung überflüssiger Spalten ('Adresszusatz', 'Public Key1', 'Public Key2', 'Public Key3', 'Public Key4')
                - neue Spalte: Inbetriebnahmejahr
                - neue Spalte: Ladegeschwindigkeit (nach Nennleistung)
                - Anpassung von Datentypen (String -> Float)
                - einzelne Zeile für jeden Ladeplatz (ladeplaetze.csv)

                ''')

    

    st.subheader("Datenüberblick mit Spaltenauswahl")

    cols = st.multiselect("Spaltenauswahl:",data.columns.tolist(), default = ["Betreiber", "Bundesland", "Inbetriebnahmejahr", "Ladegeschwindigkeit"])
    st.dataframe(data[cols])
    


