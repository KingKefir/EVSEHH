import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from ckanapi import RemoteCKAN



def app():
    APP_TITLE = 'Zeitreihenanalyse Kanadischer Daten'
    
    st.title(APP_TITLE)
    # Streamlit app title and description
    st.subheader("Electric Vehicle Time Series Analysis", divider=True)
    st.write("""
    Hier nutzen wir öffentliche Kanadische Daten welche mittel CKAN API zur Verfügung gestellt werden.
    """)
    # Configure CKAN API URL and Dataset ID
    API_URL = "https://open.canada.ca/data/en/"
    DATASET_ID = "026e45b4-eb63-451f-b34f-d9308ea3a3d9"

    # Initialize CKAN client
    ckan = RemoteCKAN(API_URL)

    # Fetch data from the CKAN API
    response = ckan.action.datastore_search(
        resource_id=DATASET_ID,
        limit=1000  # Adjust this limit if you want more or fewer records
    )

    @st.cache_data
    def load_data(api_url, dataset_id):
        """Fetch data from CKAN API and return as a DataFrame."""
        ckan = RemoteCKAN(api_url)
        response = ckan.action.datastore_search(resource_id=dataset_id, limit=1000)
        df = pd.DataFrame(response['records'])
        return df

    # Load data
    st.write("Fetching data from the CKAN API...")
    df = load_data(API_URL, DATASET_ID)
    st.write("Data loaded successfully!")

    # Convert columns to numeric types where necessary
    df['Model year'] = pd.to_numeric(df['Model year'], errors='coerce')
    df['Range (km)'] = pd.to_numeric(df['Range (km)'], errors='coerce')
    df['Combined (kWh/100 km)'] = pd.to_numeric(df['Combined (kWh/100 km)'], errors='coerce')

    # Drop rows with missing values in key columns
    df = df.dropna(subset=['Model year', 'Range (km)', 'Combined (kWh/100 km)'])

    # Group by 'Model year' and calculate average 'Range (km)' and 'Combined (kWh/100 km)' for each year
    df_yearly = df.groupby('Model year').agg({
        'Range (km)': 'mean',
        'Combined (kWh/100 km)': 'mean'
    }).reset_index()

    # Show raw data
    if st.checkbox("Show raw data"):
        st.write(df)

    # Plotting with Matplotlib and Seaborn
    st.subheader("Zeitreihenanalyse von Elektrofahrzeugen")

    # Set the plot style
    sns.set(style="whitegrid")

    # Create a figure with two subplots: one for range and one for consumption
    fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Plot Range (km) over Model Year
    sns.lineplot(data=df_yearly, x='Model year', y='Range (km)', ax=ax[0], marker='o', color='b')
    ax[0].set_title('Durchschnittliche Reichweite je Modell(Jahr)')
    ax[0].set_ylabel('Reichweite (km)')

    # Plot Combined (kWh/100 km) over Model Year
    sns.lineplot(data=df_yearly, x='Model year', y='Combined (kWh/100 km)', ax=ax[1], marker='o', color='r')
    ax[1].set_title('Durchschnittlicher EV-Gesamtverbrauch je Modell(Jahr)')
    ax[1].set_ylabel('Gesamtverbrauch (kWh/100 km)')
    ax[1].set_xlabel('Modell (Jahr)')

    # Display plot in Streamlit
    st.pyplot(fig)
