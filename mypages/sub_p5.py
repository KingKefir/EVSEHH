import pandas as pd
import plotly.express as px
import warnings
import streamlit as st

warnings.filterwarnings("ignore")

data = pd.read_csv("data/ladesaeulen.csv", delimiter=";")


def app():
    
    st.title("Ladesäulen nach Leistung")

    st.write("Normalladen:           bis 22 kW")
    st.write("Schnelladen:           22-150 kW")
    st.write("High Power Charging:   über 150 kW")


    ladep_nach_leistung = data.groupby(["P1 [kW]", "Ladegeschwindigkeit"]).size().reset_index(name='anzahl')
    ladep_nach_leistung = ladep_nach_leistung.dropna()

    alle_über_500 = ladep_nach_leistung["anzahl"] >= 500

    ladep_nach_leistung_m = ladep_nach_leistung[alle_über_500]


    # Farben definieren
    ladegeschw_farben = {
        'Normalladen': 'blue',
        'Schnellladen': 'orange',
        'High Power Charging': 'red'
        }

    fig1 = px.bar(
        ladep_nach_leistung_m,
        x='P1 [kW]',
        y='anzahl',
        color='Ladegeschwindigkeit',  # Gruppierung nach Ladegeschwindigkeit
        title="Anzahl an Ladesäulen nach Leistung und Ladegeschwindigkeit",
        labels={
            'P1 [kW]': 'Leistung [kW]', 
            'anzahl': 'Anzahl Ladeplätze', 
            'Ladegeschwindigkeit': 'Ladegeschwindigkeit'
        },
        color_discrete_map=ladegeschw_farben  # Farben zuweisen
)

    st.plotly_chart(fig1)





    nach_jahr_ladeg = data.groupby(['Inbetriebnahmejahr','Ladegeschwindigkeit']).size().reset_index(name='Anzahl')

    

    fig2 = px.bar(
        nach_jahr_ladeg,
        x='Inbetriebnahmejahr',
        y='Anzahl', 
        color='Ladegeschwindigkeit',       
        title="Neue Ladesäulen pro Jahr nach Ladegeschwindigkeit",
        labels={
            'Inbetriebnahmejahr': 'Inbetriebnahmejahr',
            'kumulierte_anzahl': 'Gesamtanzahl der Ladesäulen',  
            'Ladegeschwindigkeit': 'Ladegeschwindigkeit' 
        },
        color_discrete_map=ladegeschw_farben
        )

    st.plotly_chart(fig2)


    