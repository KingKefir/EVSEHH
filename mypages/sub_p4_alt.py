import streamlit as st


def app():
    st.title("Ladesäulen nach Anzahl der Ladeplätze")

    gif_path = "data/Comp1_3.gif"  # Replace with the path to your GIF file

    st.image(gif_path, width = 600, use_column_width=False, caption="Deutschland") 
