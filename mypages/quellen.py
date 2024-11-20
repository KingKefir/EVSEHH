import streamlit as st

def app():
    APP_TITLE = 'Quellenangabe'
    
    st.title(APP_TITLE)
    # Streamlit app title and description
    adaclink = "https://assets.adac.de/Autodatenbank/Autokosten/E-AutosVergleich.pdf"
    spritmonitorlink = "https://www.spritmonitor.de/de/auswertungen.html"
    govcanada = "https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64/resource/026e45b4-eb63-451f-b34f-d9308ea3a3d9"
    bna = "https://www.bundesnetzagentur.de/DE/Home/home_node.html"
    statistikportal = "https://www.statistikportal.de/de/open-data"
    geojsongithub = "https://github.com/isellsoap/deutschlandGeoJSON/blob/main/2_bundeslaender/4_niedrig.geo.json"
    shutterstock = "https://www.shutterstock.com/"
    eurostat = "https://ec.europa.eu/eurostat/data/database"

    st.write(f'''
    {adaclink}\n
    {spritmonitorlink}\n
    {govcanada}\n
    {bna}\n
    {statistikportal}\n
    {geojsongithub}\n
    {shutterstock}\n
    {eurostat}
    ''')