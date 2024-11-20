import pandas as pd
import plotly.express as px
import warnings
import streamlit as st

warnings.filterwarnings("ignore")

data = pd.read_csv("data/ladesaeulen.csv", delimiter=";")


def app():
    
    st.title("Ladesäulen nach Leistung")


    ladep_nach_leistung = data.groupby("P1 [kW]").size().reset_index(name='anzahl')
    ladep_nach_leistung = ladep_nach_leistung.dropna()

    alle_über_500 = ladep_nach_leistung["anzahl"] >= 500

    ladep_nach_leistung_m = ladep_nach_leistung[alle_über_500]

    fig1 = px.bar(
        ladep_nach_leistung_m,
        x='P1 [kW]',
        y='anzahl',
        title="Anzahl an Ladesäulen nach Leistung",
        labels={'P1 [kW]': 'Leistung [kW]', 'anzahl': 'Anzahl Ladeplätze'},
        color='anzahl',
        color_continuous_scale='bluered'
    )

    st.plotly_chart(fig1)





    nach_jahr_ladeg = data.groupby(['Inbetriebnahmejahr','Ladegeschwindigkeit']).size().reset_index(name='Anzahl')

    # Farben definieren
    ladegeschw_farben = {
        'Normalladen': 'blue',
        'Schnellladen': 'orange',
        'High Power Charging': 'red'
        }

    fig2 = px.bar(
        nach_jahr_ladeg,
        x='Inbetriebnahmejahr',
        y='Anzahl', 
        color='Ladegeschwindigkeit',       
        title="Neue Ladeplätze pro Jahr nach Ladegeschwindigkeit",
        labels={
            'Inbetriebnahmejahr': 'Inbetriebnahmejahr',
            'kumulierte_anzahl': 'Gesamtanzahl der Ladeplätze',  
            'Ladegeschwindigkeit': 'Ladegeschwindigkeit' 
        },
        color_discrete_map=ladegeschw_farben
        )

    st.plotly_chart(fig2)


    