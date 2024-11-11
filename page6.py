import streamlit as st
import pandas as pd

# Load CSV files
file_1 = 'data\\benzin.csv'
file_2 = 'data\\diesel.csv'
file_3 = 'data\\elektro.csv'

# Function to load and process each file with a given multiplier
def load_data(file, multiplier):
    # Load CSV file
    data = pd.read_csv(file)
    # Calculate the cost column
    data['Euro'] = data.iloc[:,2]* multiplier
    data = data.iloc[:, 1:4]
    return data

# Title
st.set_page_config(layout="wide")
st.title("Verbrauch je Marke/Modell und Kostenberechnung pro 100km")
title = "spritmonitor.de"
link = "https://www.spritmonitor.de/de/auswertungen.html"
st.markdown(f"Unten sind die laut [{title}]({link}) 50 sparsamsten Fahrzeuge in den Kategorien Benzin, Diesel und BEV.")

# Set default values for each table
default_values = [1.78, 1.88, 0.44]

# Create columns for side-by-side display
cols = st.columns(3)

# Display each table with an entry field for the multiplier above it


for i, (file, default) in enumerate(zip([file_1, file_2, file_3], default_values), start=1):
    with cols[i-1]:  # Place each table in its respective column
        # st.subheader(f"Table {i}")
        if i == 1:
            st.subheader(f"Benzin")
        elif i == 2: 
            st.subheader(f"Diesel")
        else:
            st.subheader(f"BEV")

        # Entry field with a specific default value for each table
        multiplier = st.number_input(f"Enter multiplier for Table {i}", min_value=0.0, value=default, key=f"multiplier_{i}")

        # Load data and calculate cost
        data = load_data(file, multiplier)
        
        # Display the table
        st.write(data)