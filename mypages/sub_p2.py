import streamlit as st


def app():
    st.header("Erster Ansatz: Analyse mit SQL und Tableau")

    # Pfad zur PNG-Datei
    image1 = "data/ERD.png"

    # Bild anzeigen
    st.image(image1, caption="ERD der Datenbank", use_column_width=True)

    # Pfad zur PNG-Datei
    image2 = "data/tableau_dashboard.png"

    # Bild anzeigen
    st.image(image2, caption="Dashboard", use_column_width=True)