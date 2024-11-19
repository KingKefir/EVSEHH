import streamlit as st


def app():
    st.title("Erster Ansatz: Analyse mit SQL und Tableau")

    # Pfad zur PNG-Datei
    image_path = "data/ERD.png"

    # Bild anzeigen
    st.image(image_path, caption="ERD der Datenbank", use_column_width=True)