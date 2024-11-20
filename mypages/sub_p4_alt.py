import streamlit as st


def app():    
    st.title("Karte - Anzahl der Ladesäulen")
    st.subheader("Zeitliche Entwicklung")

    gif_path = "data/Comp1_3.gif"  # Replace with the path to your GIF file

    st.image(gif_path, use_column_width=False, caption="Deutschland") 
