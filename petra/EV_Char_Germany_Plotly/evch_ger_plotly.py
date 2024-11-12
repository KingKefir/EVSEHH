import pandas as pd
import plotly.express as px
import warnings
import streamlit as st
import base64

warnings.filterwarnings("ignore")

# Daten laden
data = pd.read_csv("charging_data.csv")

# Unnötige Spalten entfernen
data = data.drop(columns=['Unnamed: 0', 'adresszusatz'])

# Spalten umbenennen
data = data.rename(columns={
        'p1_kw': 'leistung_p1',
        'p2_kw': 'leistung_p2',
        'p3_kw': 'leistung_p3',
        'p4_kw': 'leistung_p4'
    })







# Seitenleiste für die Navigation erstellen, alle Seiten anzeigen
st.sidebar.title("Navigation")
page = st.sidebar.radio("Wähle eine Seite:", 
                        ["Startseite",
                         "Erster Ansatz: Analyse mit SQL und Tableau",
                         "Überblick über die Daten",
                         "Analyse der Ladesäulen",
                         "Analyse der Ladesäulen in ausgewählten Städten / Kreisen",
                         "Analyse der Betreiberdaten"])

# Startseite
if page == "Startseite":
    st.title("Ladeinfrastruktur in Deutschland")
    st.header("Einblick in die Daten der Bundesnetzagentur zu Ladestationen in Deutschland")
    st.write("Dies ist die Startseite. Wähle eine Seite in der Navigation links, um zu beginnen.")

    st.write("Hier könnte noch ein Screenshot des Tableaudashboards hin...")







elif page == "Überblick über die Daten":
    st.title("Überblick über die Daten")

    


    # Datenüberblick
    st.write("Die Quelle für den hier analysierten Datensatz findet man unter diesem [Link](https://opendata.rhein-kreis-neuss.de/explore/dataset/rhein-kreis-neuss-ladesaulen-in-deutschland/information/?disjunctive.betreiber&disjunctive.art_der_ladeeinrichung&disjunctive.anzahl_ladepunkte&disjunctive.anschlussleistung&disjunctive.steckertypen1&disjunctive.steckertypen2&disjunctive.steckertypen3&disjunctive.steckertypen4&disjunctive.p1_kw&disjunctive.p2_kw&disjunctive.p3_kw&disjunctive.p4_kw&disjunctive.kreis_kreisfreie_stadt&disjunctive.ort)")
    st.write('''
            Da die aktuelleren Daten leider das Datum der Inbetriebnahme nicht mehr enthalten, umfasst der verwendete Teil-Datensatz nur einen Zeitraum bis Mitte des Jahres 2023.
             ''')

    st.divider()

    st.write(f"Der Datensatz besteht aus {data.shape[0]} Zeilen und {data.shape[1]} Spalten.")



    # Datenvorschau anzeigen
    st.write("Datenvorschau:")
    st.write(data.head())








# Seite: Analyse der Ladesäulen
elif page == "Analyse der Ladesäulen":
    st.title("Analyse der Ladestationen")


    # Angenommen, das Datum der Inbetriebnahme jeder Ladesäule befindet sich in der Spalte 'inbetriebnahme_datum'
    # und ist im Format 'YYYY-MM-DD'. Wir extrahieren das Jahr und berechnen die Anzahl neuer und kumulativer Ladesäulen.

    # 1. Jahr der Inbetriebnahme extrahieren
    data['jahr'] = pd.to_datetime(data['inbetriebnahmedatum']).dt.year

    # 2. Anzahl der neu in Betrieb genommenen Ladesäulen pro Jahr berechnen
    new_stations_per_year = data.groupby('jahr').size().reset_index(name='neu_inbetrieb_genommene')
    new_stations_per_year = new_stations_per_year.dropna()  # Falls leere Jahre vorhanden sind

    # 3. Kumulative Anzahl der Ladesäulen berechnen
    new_stations_per_year['kumulative_anzahl'] = new_stations_per_year['neu_inbetrieb_genommene'].cumsum()

    # 4. Diagramm der neu in Betrieb genommenen Ladesäulen pro Jahr
    fig_new = px.bar(
        new_stations_per_year,
        x='jahr',
        y='neu_inbetrieb_genommene',
        title="Neue in Betrieb genommene Ladesäulen pro Jahr",
        labels={'jahr': 'Jahr', 'neu_inbetrieb_genommene': 'Anzahl neuer Ladesäulen'},
        color='neu_inbetrieb_genommene',
        color_continuous_scale='Viridis'
    )
    fig_new.update_layout(xaxis_title="Jahr", yaxis_title="Anzahl neuer Ladesäulen")

    # 5. Diagramm der kumulativen Anzahl von Ladesäulen nach Jahren
    fig_cumulative = px.bar(
        new_stations_per_year,
        x='jahr',
        y='kumulative_anzahl',
        title="Kumulative Anzahl der Ladesäulen nach Jahren",
        labels={'jahr': 'Jahr', 'kumulative_anzahl': 'Kumulative Anzahl der Ladesäulen'},
        color='kumulative_anzahl',
        color_continuous_scale='Viridis'
    )
    fig_cumulative.update_layout(xaxis_title="Jahr", yaxis_title="Kumulative Anzahl der Ladesäulen")

    # Anzeigen der Diagramme
    
    st.plotly_chart(fig_cumulative)  # Kumulatives Diagramm anzeigen
    st.plotly_chart(fig_new)  # Neues Diagramm anzeigen








elif page == "Analyse der Ladesäulen in ausgewählten Städten / Kreisen":
    st.title("Analyse der Ladesäulen in ausgewählten Städten / Kreisen")

    # Liste der einzigartigen Städte/Orte
    städte = data['kreis_kreisfreie_stadt'].unique()

    # Auswahlfeld 
    selected_stadt = st.selectbox("Wähle eine Stadt/Ort:", städte)

    # Filtern der Daten basierend auf der Auswahl
    filtered_data = data[data['kreis_kreisfreie_stadt'] == selected_stadt]

    # Anzeige der Anzahl der Ladestationen für die ausgewählte Stadt/Ort
    st.write(f"Anzahl der Ladestationen in {selected_stadt}: {filtered_data.shape[0]}")

    # Sicherstellen, dass das Inbetriebnahmedatum im richtigen Format ist
    filtered_data['inbetriebnahmedatum'] = pd.to_datetime(filtered_data['inbetriebnahmedatum'], errors='coerce')

    # Erstelle neue Spalten für Jahr und Monat
    filtered_data['year'] = filtered_data['inbetriebnahmedatum'].dt.year

    # Zähle die Anzahl der Stationen pro Jahr
    year_group = filtered_data.groupby('year').size().reset_index(name='count')

    # Berechne die kumulative Summe der Ladestationen bis zum jeweiligen Jahr
    year_group['cumulative_count'] = year_group['count'].cumsum()

    # Visualisierung der kumulierten Ladestationen pro Jahr
    fig = px.bar(year_group,
                    x='year',
                    y='cumulative_count',
                    title=f"Gesamte Anzahl der Ladestationen in {selected_stadt} pro Jahr",
                    labels={'year': 'Jahr', 'cumulative_count': 'Gesamte Anzahl der Ladestatationen'},
                    color='cumulative_count',
                    color_continuous_scale='Viridis')

    # Diagramm in Streamlit anzeigen
    st.plotly_chart(fig)









elif page == "Analyse der Betreiberdaten":
    st.title("Analyse der Betreiberdaten")

    betreiber_group = pd.DataFrame(data['betreiber'].value_counts().reset_index().values, columns=['betreiber', 'count'])
    betreiber_group.loc[betreiber_group['count'] < 200, 'betreiber'] = 'Andere Betreiber'
    
    fig = px.pie(betreiber_group, 
             names='betreiber', 
             values='count', 
             color_discrete_sequence=px.colors.sequential.Viridis,
             height=500)
    st.plotly_chart(fig)

    st.divider()
    
    top_ten_betreiber = betreiber_group['betreiber'].head(10).values

    st.write(top_ten_betreiber)