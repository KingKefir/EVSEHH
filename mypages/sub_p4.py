import pandas as pd
import plotly.express as px
import streamlit as st

# Daten laden
data = pd.read_csv("data/ladesaeulen.csv", delimiter=";")


def app():
    st.title("Ladesäulen nach Anzahl der Ladeplätze")

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
    #anzahl_nach_plätzen = data.groupby('Anzahl Ladeplätze pro Säule').size().reset_index(name='anzahl')

    anzahl_nach_plätzen = data.groupby(['Anzahl Ladeplätze pro Säule', 'Ladegeschwindigkeit']) \
                          .size() \
                          .reset_index(name='anzahl')


    # Plot erstellen
    fig1 = px.bar(
        anzahl_nach_plätzen,
        x='Anzahl Ladeplätze pro Säule',
        y='anzahl',
        color='Ladegeschwindigkeit',
        title="Anzahl Ladeplätze pro Säule"
    )
    fig1.update_layout(
        xaxis_title="Anzahl Ladeplätze pro Säule",
        yaxis_title="Anzahl der Ladesäulen"
    )
    st.plotly_chart(fig1)

    