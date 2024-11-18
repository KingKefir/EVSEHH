import pandas as pd
import plotly.express as px
import warnings
import streamlit as st

warnings.filterwarnings("ignore")

data = pd.read_csv("ladesaeulenregister.csv", delimiter=";", on_bad_lines="skip")

# Unnötige Spalten entfernen
data = data.drop(columns=['Adresszusatz', 'Public Key1', 'Public Key2', 'Public Key3', 'Public Key4' ])
data = data.dropna(subset=['Inbetriebnahmedatum'])
data = data.dropna(subset=['Betreiber'])

# Jahr der Inbetriebnahme in neue Spalte
data['Inbetriebnahmejahr'] = pd.to_datetime(data['Inbetriebnahmedatum'], format='%d.%m.%Y', errors='coerce').dt.year

# Umwandlung der Daten: Jede Ladepunkt-Information in eine eigene Zeile
rows = []
for _, row in data.iterrows():
    for i in range(1, 5):  # Für Steckertypen1 bis Steckertypen4
        steckertyp = row[f"Steckertypen{i}"]
        p_kw = row[f"P{i} [kW]"]
        
        if pd.notna(steckertyp):  # Nur Einträge mit Steckertypen behalten
            new_row = row.drop([f"Steckertypen{j}" for j in range(1, 5)] +
                               [f"P{j} [kW]" for j in range(1, 5)]).to_dict()
            new_row.update({
                "Steckertyp": steckertyp,
                "Leistung [kW]": p_kw,
            })
            rows.append(new_row)

# Neues DataFrame erstellen
df_ladeplaetze = pd.DataFrame(rows)

def app():
    st.title("Ladeplätze nach Leistung")

    st.subheader("Angepasster Datensatz mit einer Zeile pro Ladeplatz")
    st.write("Da die Nennleistung der Ladesäulen teilweise die Leistung der einzelnen Ladepunkte, teilweise aber auch die Gesamtleistung aller Ladeplätze angibt, betrachten wir hier jeden Ladeplatz separat.")
    st.write(df_ladeplaetze)

    st.divider()

    ladep_nach_leistung = df_ladeplaetze.groupby("Leistung [kW]").size().reset_index(name='anzahl')
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
        color_continuous_scale='Viridis'
    )

    st.plotly_chart(fig1)

    # Konvertiere die 'Leistung [kW]' Spalte in numerische Werte und setze ungültige Werte auf NaN
    df_ladeplaetze['Leistung [kW]'] = pd.to_numeric(df_ladeplaetze['Leistung [kW]'], errors='coerce')

        # Neue Spalte für Ladegeschwindigkeit hinzufügen
    def ladegeschwindigkeit(row):
        if "AC" in row['Steckertyp']:
            return 'Normalladen'
        elif "DC" in row['Steckertyp']:
            return 'Schnellladen'
        else:
            return 'Andere'

    # Ladegeschwindigkeit anwenden
    df_ladeplaetze['Ladegeschwindigkeit'] = df_ladeplaetze.apply(ladegeschwindigkeit, axis=1)

    # Gruppierung nach Ladegeschwindigkeit und Inbetriebnahmejahr
    ladep_nach_geschwindigkeit_und_jahr = (
        df_ladeplaetze.groupby(['Inbetriebnahmejahr', 'Ladegeschwindigkeit'])
        .size()
        .reset_index(name='anzahl')
    )

    # Berechnung der kumulierten Summe
    ladep_nach_geschwindigkeit_und_jahr['kumulierte_anzahl'] = ladep_nach_geschwindigkeit_und_jahr['anzahl'].cumsum()

    # Filtern der Daten, um nur Jahre ab 2008 anzuzeigen
    ladep_nach_geschwindigkeit_und_jahr_filtered = ladep_nach_geschwindigkeit_und_jahr[
    ladep_nach_geschwindigkeit_und_jahr['Inbetriebnahmejahr'] >= 2008
    ]




    fig2 = px.bar(
        ladep_nach_geschwindigkeit_und_jahr_filtered,
        x='Inbetriebnahmejahr',
        y='kumulierte_anzahl', 
        color='Ladegeschwindigkeit',       
        title="Gesamtanzahl der Ladeplätze nach Leistung [kW]",
        labels={
            'Inbetriebnahmejahr': 'Inbetriebnahmejahr',
            'kumulierte_anzahl': 'Gesamtanzahl der Ladeplätze',  
            'Leistung [kW]': 'Leistung [kW]' 
        },
        color_continuous_scale='Blues'
        )

    st.plotly_chart(fig2)

        