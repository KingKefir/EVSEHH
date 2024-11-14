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
    st.title("Analyse der Ladestationen")

    # 1. Jahr der Inbetriebnahme in neue Spalte
    data['Inbetriebnahmejahr'] = pd.to_datetime(data['Inbetriebnahmedatum'], format='%d.%m.%Y', errors='coerce').dt.year

    # 2. Anzahl der neu in Betrieb genommenen Ladesäulen pro Jahr berechnen
    lasta_neu_pro_jahr = data.groupby('Inbetriebnahmejahr').size().reset_index(name='neu_inbetrieb_genommene')
    lasta_neu_pro_jahr = lasta_neu_pro_jahr.dropna()

    # 3. Kumulative Anzahl der Ladesäulen berechnen
    lasta_neu_pro_jahr['kumulative_anzahl'] = lasta_neu_pro_jahr['neu_inbetrieb_genommene'].cumsum()

    # 4. Prozentuale Zunahme für ganz Deutschland berechnen
    lasta_neu_pro_jahr['wachstum_prozent'] = lasta_neu_pro_jahr['neu_inbetrieb_genommene'].pct_change() * 100

    # 5. Prozentuale Zunahme und kumulative Anzahl für jedes Bundesland berechnen
    bundeslandzahlen = data.groupby(['Bundesland', 'Inbetriebnahmejahr']).size().reset_index(name='anzahl')
    bundeslandzahlen['kumulative_anzahl'] = bundeslandzahlen.groupby('Bundesland')['anzahl'].cumsum()
    bundeslandzahlen['wachstum_prozent'] = bundeslandzahlen.groupby('Bundesland')['anzahl'].pct_change() * 100

    # 4. Diagramm der neu in Betrieb genommenen Ladesäulen pro Jahr
    fig_new = px.bar(
        lasta_neu_pro_jahr,
        x='Inbetriebnahmejahr',
        y='neu_inbetrieb_genommene',
        title="Neue in Betrieb genommene Ladesäulen pro Jahr",
        labels={'Inbetriebnahmejahr': 'Jahr', 'neu_inbetrieb_genommene': 'Anzahl neuer Ladesäulen'},
        color='neu_inbetrieb_genommene',
        color_continuous_scale='Viridis'
    )
    fig_new.update_layout(xaxis_title="Jahr", yaxis_title="Anzahl neuer Ladesäulen")
    

    # 5. Diagramm der kumulativen Anzahl von Ladesäulen nach Jahren
    fig_cumulative = px.bar(
        lasta_neu_pro_jahr,
        x='Inbetriebnahmejahr',
        y='kumulative_anzahl',
        title="Gesamtanzahl der Ladesäulen nach Jahren",
        labels={'Inbetriebnahmejahr': 'Jahr', 'kumulative_anzahl': 'Gesamtanzahl der Ladesäulen'},
        color='kumulative_anzahl',
        color_continuous_scale='Viridis'
    )
    fig_cumulative.update_layout(xaxis_title="Jahr", yaxis_title="Gesamtanzahl der Ladesäulen")
    
    
    st.plotly_chart(fig_new)
    
    st.plotly_chart(fig_cumulative)

    # Plot für die kumulative Anzahl der Ladesäulen in ganz Deutschland
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=lasta_neu_pro_jahr['Inbetriebnahmejahr'], 
        y=lasta_neu_pro_jahr['kumulative_anzahl'],
        mode='lines+markers',
        name='Kumulative Anzahl Ladesäulen'
    ))
    fig1.update_layout(title="Kumulative Anzahl der Ladesäulen in Deutschland",
                    xaxis_title="Jahr",
                    yaxis_title="Kumulative Anzahl")
    
    st.plotly_chart(fig1)

    # Plot für die prozentuale Wachstumsrate in ganz Deutschland
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=lasta_neu_pro_jahr['Inbetriebnahmejahr'], 
        y=lasta_neu_pro_jahr['wachstum_prozent'],
        name='Wachstumsrate (%)'
    ))
    fig2.update_layout(title="Prozentuale Zunahme der Ladesäulen in Deutschland",
                    xaxis_title="Jahr",
                    yaxis_title="Wachstumsrate (%)")
    st.plotly_chart(fig2)

    # Interaktiver Plot für die kumulative Anzahl und Wachstumsrate pro Bundesland
    selected_bundesland = st.selectbox("Wählen Sie ein Bundesland", bundeslandzahlen['Bundesland'].unique())

    # Filter für ausgewähltes Bundesland
    bundesland_data = bundeslandzahlen[bundeslandzahlen['Bundesland'] == selected_bundesland]

    # Plot für kumulative Anzahl im ausgewählten Bundesland
    fig3 = px.line(
        bundesland_data, 
        x="Inbetriebnahmejahr", 
        y="kumulative_anzahl", 
        title=f"Kumulative Anzahl der Ladesäulen in {selected_bundesland}"
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
