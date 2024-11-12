# main_app.py
import streamlit as st
import importlib

st.set_page_config(layout="wide")
# Function to load a page module and call its 'show' function
def load_page(page_name):
    page_module = importlib.import_module(f"pages.{page_name}")
    page_module.show()

# Sidebar for navigation
st.sidebar.title("Navigation")
pages = {
    "Start Page": "start",
    "Page 1": "page1",
    "Page 2": "page2",
    "Page 6": "page6",
    "Page 7": "page7",
    "Page 8": "page8"
}

# Select page from the sidebar
selected_page = st.sidebar.radio("Go to", list(pages.keys()))

# Load and display the selected page
if selected_page == "Start Page":
    st.title("Welcome to the Streamlit App!")
    st.write("This is the start page. Use the sidebar to navigate through the app.")
else:
    load_page(pages[selected_page])
