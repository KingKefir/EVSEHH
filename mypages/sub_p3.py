import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Daten laden
data = pd.read_csv("ladesaeulenregister.csv", delimiter=";", on_bad_lines="skip")
# Unnötige Spalten entfernen
data = data.drop(columns=['Adresszusatz', 'Public Key1', 'Public Key2', 'Public Key3', 'Public Key4'])
data = data.dropna(subset=['Inbetriebnahmedatum', 'Betreiber', 'Bundesland'])

# App-Definition
def app():
    st.title("Anzahl der Ladesäulen")

    st.subheader("Anzahl Ladesäulen in Deutschland - ab 2007")

    # Jahr der Inbetriebnahme in neue Spalte
    data['Inbetriebnahmejahr'] = pd.to_datetime(data['Inbetriebnahmedatum'], format='%d.%m.%Y', errors='coerce').dt.year

    # Fliler: Nur Daten ab 2007, da vorher nicht durchgängig
    ab_2007 = data["Inbetriebnahmejahr"]>=2007
    data_ab_2007 = data[ab_2007]

    # Anzahl der neu in Betrieb genommenen Ladesäulen pro Jahr berechnen
    lasta_neu_pro_jahr = data_ab_2007.groupby('Inbetriebnahmejahr').size().reset_index(name='neu_inbetrieb_genommene')
    lasta_neu_pro_jahr = lasta_neu_pro_jahr.dropna()

    # Kumulative Anzahl der Ladesäulen berechnen
    lasta_neu_pro_jahr['kumulative_anzahl'] = lasta_neu_pro_jahr['neu_inbetrieb_genommene'].cumsum()

    # Prozentuale Zunahme für ganz Deutschland berechnen
    lasta_neu_pro_jahr['wachstum_prozent'] = lasta_neu_pro_jahr['kumulative_anzahl'].pct_change() * 100

    # 5. Prozentuale Zunahme und kumulative Anzahl für jedes Bundesland berechnen
    bundeslandzahlen = data_ab_2007.groupby(['Bundesland', 'Inbetriebnahmejahr']).size().reset_index(name='anzahl')
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

    

    st.subheader("Anzahl Ladesäulen nach Bundesland ab 2007")

    # Interaktiver Plot für die kumulative Anzahl und Wachstumsrate pro Bundesland
    selected_bundesland = st.selectbox("Wählen Sie ein Bundesland", bundeslandzahlen['Bundesland'].unique())

    # Filter für ausgewähltes Bundesland
    bundesland_data = bundeslandzahlen[bundeslandzahlen['Bundesland'] == selected_bundesland]

    fig2 = px.bar(
        bundesland_data,
        x='Inbetriebnahmejahr',
        y='anzahl',
        title=f"Neue in Betrieb genommene Ladesäulen pro Jahr in {selected_bundesland}",
        )
    fig2.update_layout(xaxis_title="Jahr", yaxis_title="Anzahl neuer Ladestellen")
    st.plotly_chart(fig2)
    
    # Plot für kumulative Anzahl im ausgewählten Bundesland
    fig3 = px.bar(
        bundesland_data, 
        x="Inbetriebnahmejahr", 
        y="kumulative_anzahl", 
        title=f"Gesamtanzahl der Ladesäulen in {selected_bundesland}"
    )
    fig3.update_layout(xaxis_title="Jahr", yaxis_title="Kumulative Anzahl")
    st.plotly_chart(fig3)

    # Plot für Wachstumsrate im ausgewählten Bundesland
    fig4 = px.bar(
        bundesland_data, 
        x="Inbetriebnahmejahr", 
        y="wachstum_prozent", 
        title=f"Prozentuale Zunahme der Ladesäulen in {selected_bundesland}"
    )
    fig4.update_layout(xaxis_title="Jahr", yaxis_title="Wachstumsrate (%)")
    st.plotly_chart(fig4)
