import streamlit as st

def app():
    st.header("Einblick in die Daten der Bundesnetzagentur zu Ladestationen in Deutschland")

    st.write("Dies ist die Startseite. Wähle eine Seite in der Navigation links, um zu beginnen.")

     # Pfad zur PNG-Datei
    image_path = "data/bild_ladestelle.png"

    # Bild anzeigen
    st.image(image_path, caption="'Stromtankstelle' für Elektrofahrzeuge (Quelle: www.shutterstock.com)", use_column_width=True)
