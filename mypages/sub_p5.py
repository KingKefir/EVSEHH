import pandas as pd
import plotly.express as px
import warnings
import streamlit as st
import folium
from streamlit_folium import st_folium

warnings.filterwarnings("ignore")

data_lp = pd.read_csv("data/ladeplaetze.csv", delimiter=";")


def app():
    
    st.title("Ladeplatz nach Leistung")
    st.subheader("Angepasster Datensatz mit einer Zeile pro Ladeplatz")
    st.write("Da die Nennleistung der Ladesäulen teilweise die Leistung der einzelnen Ladepunkte, teilweise aber auch die Gesamtleistung aller Ladeplätze angibt, betrachten wir hier jeden Ladeplatz separat.")

    st.write(data_lp)

    st.divider()

    ladep_nach_leistung = data_lp.groupby("Leistung [kW]").size().reset_index(name='anzahl')
    ladep_nach_leistung = ladep_nach_leistung.dropna()

    alle_über_1000 = ladep_nach_leistung["anzahl"] >= 1000

    ladep_nach_leistung_m = ladep_nach_leistung[alle_über_1000]

    fig1 = px.bar(
        ladep_nach_leistung_m,
        x='Leistung [kW]',
        y='anzahl',
        title="Anzahl an Ladeplätzen nach Leistung",
        labels={'Leistung [kW]': 'Leistung [kW]', 'anzahl': 'Anzahl Ladeplätze'},
        color='anzahl',
        color_continuous_scale='bluered'
    )

    st.plotly_chart(fig1)





    nach_jahr_ladeg = data_lp.groupby(['Inbetriebnahmejahr','Ladegeschwindigkeit']).size().reset_index(name='Anzahl')

    # Farben definieren
    ladegeschw_farben = {
        'Normalladen': 'blue',
        'Schnellladen': 'orange',
        'Ultraschnellladen': 'red'
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


    

    







    