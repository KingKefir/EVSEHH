import streamlit as st

from mypages import sub_p0, sub_p1, sub_p2, sub_p3, sub_p4, sub_p5, sub_p6, sub_p_eu, sub_p_map, Page1, page6, page7, page8, quellen, dankebye

st.set_page_config(layout="wide", page_title="Ladeinfrastrukturanalyse von Petra und Roman")
# HTML für Titel mit Rahmen und anderer Schriftart
title_html = """
    <div style="
        border: 3px solid #000000;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        background-color: #dbe9f4;
        font-size: 24px;
        color: #000000;
        font-weight: bold;">
        LADEINFRASTRUKTUR IN DEUTSCHLAND
    </div>
"""

# Anzeige des Titels mit HTML und CSS
st.markdown(title_html, unsafe_allow_html=True)

pages = {
    "0. Startseite": sub_p0,
    "1. Einordnung: Deutschland und seine Nachbarländer (2023)": sub_p_eu,
    "2. Überblick über die Daten": sub_p1,
    "3. Erster Ansatz: Analyse mit SQL und Tableau": sub_p2,
    "4. Karte: Karte - Anzahl der Ladesäulen nach Jahren": sub_p_map,
    "5. Analyse der Ladesäulen": sub_p3,
    "6. Ladesäulen nach Anzahl der Ladepunkte": sub_p4,
    "7. Ladeplätze nach Leistung": sub_p5,
    "8. Steckertypen": sub_p6,
    "9. Ladesäulen in Deutschland": Page1,
    "10. Verbrauchsrechner": page6,
    "11. Zeitreihenanalyse Kanadischer Daten": page7,
    "12. Reichweiten- und Effizienzanalyse": page8,
    "13. Tschüssi": dankebye,
    "14. Quellenangabe": quellen
        }


st.sidebar.title("Navigation")
select = st.sidebar.radio("Gehe zu:", list(pages.keys()))
pages[select].app()