import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
import streamlit as st

# Daten laden
data = pd.read_csv("ladesaeulenregister.csv", delimiter=";", on_bad_lines="skip")
# Unnötige Spalten entfernen
data = data.drop(columns=['Adresszusatz', 'Public Key1', 'Public Key2', 'Public Key3', 'Public Key4' ])
data = data.dropna(subset=['Inbetriebnahmedatum'])
data = data.dropna(subset=['Betreiber'])

data['P3 [kW]'] = data['P3 [kW]'].str.replace(',', '.', regex=False)
#Konvertieren in float, NaN-Werte bleiben erhalten
data['P3 [kW]'] = pd.to_numeric(data['P3 [kW]'], errors='coerce')

data['Inbetriebnahmejahr'] = pd.to_datetime(data['Inbetriebnahmedatum'], format='%d.%m.%Y', errors='coerce').dt.year


def app():
    st.title("Ladesäulen nach Anzahl der Ladepunkte")

    def berechne_ladeplaetze(row):
        if pd.isnull(row['Steckertypen2']):
            return 1
        elif pd.isnull(row['Steckertypen3']):
            return 2
        elif pd.isnull(row['Steckertypen4']):
            return 3
        else:
            return 4

    data["Anzahl Ladeplätze pro Säule"] = data.apply(berechne_ladeplaetze, axis=1)

    # Gruppierung der Daten
    anzahl_nach_plätzen = data.groupby('Anzahl Ladeplätze pro Säule').size().reset_index(name='anzahl')

    # Daten anzeigen
    st.write(data)

    # Plot erstellen
    fig1 = px.bar(
        anzahl_nach_plätzen,
        x='Anzahl Ladeplätze pro Säule',
        y='anzahl',
        title="Anzahl Ladeplätze pro Säule"
    )
    fig1.update_layout(
        xaxis_title="Anzahl Ladeplätze pro Säule",
        yaxis_title="Anzahl der Ladesäulen"
    )
    st.plotly_chart(fig1)

    # Fliler: Nur Daten ab 2007, da der Plot sonst nur Werte im Bereich x>2010 auseinanderhalten kann

    ab_2007 = data["Inbetriebnahmejahr"]>=2007
    data_ab_2007 = data[ab_2007]

    ladepl_zahlen = data_ab_2007.groupby(['Anzahl Ladeplätze pro Säule', 'Inbetriebnahmejahr']).size().reset_index(name='anzahl_säulen_neu')

    ladepl_zahlen['kumulative_anzahl_säulen'] = ladepl_zahlen.groupby(['Anzahl Ladeplätze pro Säule'])['anzahl_säulen_neu'].cumsum()

    fig2 = px.line(
    ladepl_zahlen,
    x='Inbetriebnahmejahr',
    y='kumulative_anzahl_säulen', 
    color='Anzahl Ladeplätze pro Säule',       
    title="Gesamtanzahl der Ladesäulen nach Anzahl der Ladeplätze ab 2008",
    labels={
        'Inbetriebnahmejahr': 'Inbetriebnahmejahr',
        'kumulative_anzahl_säulen': 'Gesamtanzahl der Ladesäulen',  
        'Anzahl Ladeplätze pro Säule': 'Anzahl Ladeplätze pro Säule' 
    }
    )

    # Plot anzeigen
    st.plotly_chart(fig2)
