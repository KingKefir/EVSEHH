import pandas as pd
import streamlit as st

# Daten laden
data_org = pd.read_csv("data/ladesaeulenregister.csv", delimiter=";", on_bad_lines="skip", low_memory=False)



def app():
    st.title("Überblick über die Daten")
    st.subheader("Die Datenquelle")

    # Datenüberblick
    st.write("Die verwendeten Daten stammen von der **Bundesnetzagentur**. Man findet sie unter diesem [Link](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/E-Mobilitaet/Ladesaeulenkarte/start.html).")
    st.write(f"Der Datensatz besteht aus **{data_org.shape[0]} Zeilen** und **{data_org.shape[1]} Spalten**.")
    st.write("Die Daten werden laufend aktualisiert. Hier wurde die **Version vom 12.11.2024** verwendet.")

    # Datenvorschau 
    with st.expander("Datenvorschau **Originaldaten**"):
        st.write("Hier sieht man die ersten 10 Zeilen des Datensatzes.")
        st.write(data_org.head(10))
    

    st.divider()

    st.subheader("Anpassung des Datensatzes")
    st.subheader("Erstellung einer neuen csv-Datei (**ladesaeulen.csv**) zur Vermeidung langer Ladezeiten")

    st.markdown('''
                Folgende Anpassungen wurden durchgeführt:
                - Entfernung überflüssiger Spalten ('Adresszusatz', 'Public Key1', 'Public Key2', 'Public Key3', 'Public Key4')
                - neue Spalte: Inbetriebnahmejahr
                - neue Spalte: Ladegeschwindigkeit (nach Nennleistung)
                - Anpassung von Datentypen (String -> Float)

                ''')

    # angepasster Datensatz ladesaeulen.csv
    data = pd.read_csv("data/ladesaeulen.csv", delimiter=";")
    
    st.subheader("Datenüberblick mit Spaltenauswahl")

    cols = st.multiselect("Spaltenauswahl:",data.columns.tolist(), default = ["Betreiber", "Kreis/kreisfreie Stadt", "Inbetriebnahmejahr", "Ladegeschwindigkeit"])
    st.dataframe(data[cols])
    


