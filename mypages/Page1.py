import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json
from folium.plugins import GroupedLayerControl


def app():

    APP_TITLE = 'Ladesäulen in Deutschland'
    
    st.title(APP_TITLE)
    # EVSE Daten der Bundesnetzagentur
    file_path = 'data/ladesaeulenregister.csv'
    data = pd.read_csv(file_path, delimiter=';', low_memory=False)

    with open('data/DE_niedrig.geo.json', encoding='utf-8') as f:
        geodata = json.load(f)

    # KFZ Daten der Bundesländer
    kfzxl = 'data/fz27_202210.xlsx'
    kfzdf = pd.read_excel(kfzxl, sheet_name='FZ 27.2', header=7, usecols='B,C,M')


    # Anzahl KFZ nach Kraftstoffart und Gesamt per Bundesland
    state_dfs = {}


    for i in range(0, 144, 8):
        state_name = kfzdf.iloc[i, 0]

        state_dfs[state_name] = kfzdf.iloc[i:i+8].reset_index(drop=True)

    state_dfs = {state: df.dropna(subset=['Kraftfahrzeuge \ninsgesamt']) for state, df in state_dfs.items()}

    # Anzahl der Ladesäulen je Bundesland in einem Pandas Datensatz
    bundesland_counts = data['Bundesland'].value_counts()

    bundesland_counts = data['Bundesland'].value_counts().reset_index()
    bundesland_counts.columns = ['Bundesland', 'Count']

    all_ev = {
        state:
        df['Kraftfahrzeuge \ninsgesamt'].iloc[3] + 
        df['Kraftfahrzeuge \ninsgesamt'].iloc[5]
        for state, df in state_dfs.items()}

    # Display the results
    # Ensure the column names and dictionary keys match correctly between bundesland_counts and all_ev
    bundesland_counts['EV_Ratio'] = bundesland_counts.apply(
        lambda row: (row['Count'] / all_ev.get(row['Bundesland'], 1)) * 1000, axis=1
    )


    # Anzahl der Ladesäulen zum Geo-Datensatz hinzugefügt, um diesen im Landkarten-Tooltip anzeigbar zu machen

    # Karte erstellen
    map = folium.Map(location=[51, 10.3], zoom_start=6, scrollWheelZoom=False, tiles='CartoDB positron')

    # Anzahl von Ladestationen (count_evse) und Anzahl von Elektromobilen und Plug-in-Hyriden (ev_count)
    # wird der geodata beigefügt, um diese Daten in den Tooltipps sichtbar zu machen. 
    # Es kann jeweils nur ein Datensatz an das Tooltip Objekt übergeben werden.

    for feature in geodata['features']:
        bundesland = feature['properties']['name']
        evse_count = bundesland_counts.loc[bundesland_counts['Bundesland'] == bundesland, 'Count']
        evse_ratio = bundesland_counts.loc[bundesland_counts['Bundesland'] == bundesland, 'EV_Ratio']
        feature['properties']['Count'] = int(evse_count.iloc[0]) if not evse_count.empty else 0
        feature['properties']['EVSE_Ratio'] = round(float(evse_ratio.iloc[0]), 2) if not evse_ratio.empty else 0
        
        ev_count = (state_dfs[bundesland]['Kraftfahrzeuge \ninsgesamt'][3] +
                    state_dfs[bundesland]['Kraftfahrzeuge \ninsgesamt'][5]) 
        feature['properties']['ev_count'] = int(ev_count) #if not ev_count.empty else 0


    choropleth1 = folium.Choropleth(
        geo_data=geodata,
        name="Ladensäulen per Bundesland",
        data=bundesland_counts,
        columns=['Bundesland', 'Count'],
        key_on='feature.properties.name',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        overlay=True,
        control=True,
        show=True,
        legend_name="Ladesäulen pro Bundesland"
    ).add_to(map)

    # Add tooltip
    choropleth1.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['name', 'Count', 'ev_count', 'EVSE_Ratio'],
            aliases=['Bundesland:', 'Anzahl Ladesäulen:', 'Anzahl E-Fahrzeuge:','EVSE pro 1000 E-Fahrzeuge:'],
            labels=True,
            sticky=True,
            localize=True,
            toLocaleString=True,
            style=("background-color: white; color: black; font-weight: bold;"),
            tooltip_template="""<div>Bundesland: {name}<br>Count: {Count}<br>E-Fahrzeuge: {ev_count}<br>EVSE pro 1000 EV: {EVSE_Ratio}</div>"""
        )
    )

    choropleth2 = folium.Choropleth(
        geo_data=geodata,
        name="Ladensäulen pro E-Fahrzeug per Bundesland",
        data=bundesland_counts,
        columns=['Bundesland', 'EV_Ratio'],
        key_on='feature.properties.name',
        fill_color='Blues',
        fill_opacity=0.7,
        line_opacity=0.2,
        overlay=True,
        control=True,
        show=False,
        legend_name="Ladesäulen pro E-Fahrzeug"
    ).add_to(map)

    choropleth2.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['name', 'Count', 'ev_count', 'EVSE_Ratio'],
            aliases=['Bundesland:', 'Anzahl Ladesäulen:', 'Anzahl E-Fahrzeuge:','EVSE pro 1000 E-Fahrzeuge:'],
            labels=True,
            sticky=True,
            localize=True,
            toLocaleString=True,
            style=("background-color: white; color: black; font-weight: bold;"),
            tooltip_template="""<div>Bundesland: {name}<br>Count: {Count}<br>E-Fahrzeuge: {ev_count}<br>EVSE pro 1000 EV: {EVSE_Ratio}</div>"""
        )
    )
    folium.LayerControl(collapsed=True, position='bottomleft').add_to(map)

    GroupedLayerControl(
    groups={'groups1': [choropleth1, choropleth2]},
    collapsed=False,
    position='bottomright'
    ).add_to(map)

    st_map = st_folium(map, width=900, height=650)