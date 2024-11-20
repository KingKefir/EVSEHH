import pandas as pd
import plotly.express as px
import streamlit as st

# Daten laden
data = pd.read_csv("data/ladesaeulen.csv", delimiter=";")


def app():
    st.title("Anzahl der Ladesäulen")

    st.subheader("Anzahl Ladesäulen in Deutschland - ab 2010")


    # Fliler: Nur Daten ab 2010, da vorher nicht durchgängig
    ab_2010 = data["Inbetriebnahmejahr"]>=2010
    data_ab_2010 = data[ab_2010]

    # Anzahl der neu in Betrieb genommenen Ladesäulen pro Jahr
    lasta_neu_pro_jahr = data_ab_2010.groupby('Inbetriebnahmejahr').size().reset_index(name='neu_inbetrieb_genommene')
    lasta_neu_pro_jahr = lasta_neu_pro_jahr.dropna()

    # Kumulative Anzahl der Ladesäulen
    lasta_neu_pro_jahr['kumulative_anzahl'] = lasta_neu_pro_jahr['neu_inbetrieb_genommene'].cumsum()

    # Prozentuale Zunahme für ganz Deutschland
    lasta_neu_pro_jahr['wachstum_prozent'] = lasta_neu_pro_jahr['kumulative_anzahl'].pct_change() * 100

    # Prozentuale Zunahme und kumulative Anzahl für jedes Bundesland
    bundeslandzahlen = data_ab_2010.groupby(['Bundesland', 'Inbetriebnahmejahr']).size().reset_index(name='anzahl')
    bundeslandzahlen['kumulative_anzahl'] = bundeslandzahlen.groupby('Bundesland')['anzahl'].cumsum()
    bundeslandzahlen['wachstum_prozent'] = bundeslandzahlen.groupby('Bundesland')['kumulative_anzahl'].pct_change() * 100

    # Diagramm - neu in Betrieb genommene Ladesäulen pro Jahr
    fig_new = px.bar(
        lasta_neu_pro_jahr,
        x='Inbetriebnahmejahr',
        y='neu_inbetrieb_genommene',
        title="Neue in Betrieb genommene Ladesäulen pro Jahr",
        labels={'Inbetriebnahmejahr': 'Jahr', 'neu_inbetrieb_genommene': 'Anzahl neuer Ladesäulen'},
        color='neu_inbetrieb_genommene',
        color_continuous_scale='Viridis'
    )
    
    # Diagramm der kumulativen Anzahl von Ladesäulen nach Jahren
    fig_cumulative = px.bar(
        lasta_neu_pro_jahr,
        x='Inbetriebnahmejahr',
        y='kumulative_anzahl',
        title="Gesamtanzahl der Ladesäulen nach Jahren",
        labels={'Inbetriebnahmejahr': 'Jahr', 'kumulative_anzahl': 'Gesamtanzahl der Ladesäulen'},
        color='kumulative_anzahl',
        color_continuous_scale='Viridis'
    )
    
    # Prozentuales Wachstum von Jahr zu Jahr
    fig_percent = px.bar(
        lasta_neu_pro_jahr,
        x='Inbetriebnahmejahr',
        y='wachstum_prozent',
        title="Prozentuale Zunahme der Ladesäulen im Vergleich zum Vorjahr",
        labels={'Inbetriebnahmejahr': 'Jahr', 'wachstum_prozent': 'Prozentuale Zunahme'},
        color='wachstum_prozent',
        color_continuous_scale='Viridis'
    )
    
    
    st.plotly_chart(fig_new)
    
    st.plotly_chart(fig_cumulative)

    st.plotly_chart(fig_percent)

    

    st.subheader("Anzahl Ladesäulen nach Bundesland ab 2010")

    # Filter für ausgewähltes Bundesland
    selected_bundesland = st.selectbox("Wählen Sie ein Bundesland", bundeslandzahlen['Bundesland'].unique())

    bundesland_data = bundeslandzahlen[bundeslandzahlen['Bundesland'] == selected_bundesland]

    # Plot für Gesamtanzahl im ausgewählten Bundesland
    fig2 = px.bar(
        bundesland_data,
        x='Inbetriebnahmejahr',
        y='anzahl',
        title=f"Neue in Betrieb genommene Ladesäulen pro Jahr in {selected_bundesland}",
        labels={'Inbetriebnahmejahr': 'Jahr', 'anzahl': 'Anzahl neuer Ladesäulen'},
        )
    fig2.update_layout(xaxis_title="Jahr", yaxis_title="Anzahl neuer Ladestellen")
    st.plotly_chart(fig2)
    
    # Plot für kumulative Anzahl im ausgewählten Bundesland
    fig3 = px.bar(
        bundesland_data, 
        x="Inbetriebnahmejahr", 
        y="kumulative_anzahl", 
        title=f"Gesamtanzahl der Ladesäulen in {selected_bundesland}",
        labels={'Inbetriebnahmejahr': 'Jahr', 'kumulative_anzahl': 'Gesamtanzahl Ladesäulen'}
    )
    fig3.update_layout(xaxis_title="Jahr", yaxis_title="Gesamtanzahl")
    st.plotly_chart(fig3)

    # Plot für Wachstumsrate im ausgewählten Bundesland
    fig4 = px.bar(
        bundesland_data, 
        x="Inbetriebnahmejahr", 
        y="wachstum_prozent", 
        title=f"Prozentuale Zunahme der Ladesäulen in {selected_bundesland}",
        labels={'Inbetriebnahmejahr': 'Jahr', 'wachstum_prozent': 'Prozentuale Zunahme'}
    )
    fig4.update_layout(xaxis_title="Jahr", yaxis_title="Prozentuale Zunahme")
    st.plotly_chart(fig4)
