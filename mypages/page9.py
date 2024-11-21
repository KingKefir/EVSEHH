import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from ckanapi import RemoteCKAN

def app():
    # Streamlit App Title
    st.title("Fahrzeugklassen pro Jahr - Kanada")

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
        """Fetch and prepare data from CKAN API."""
        ckan = RemoteCKAN(api_url)
        response = ckan.action.datastore_search(
            resource_id=dataset_id,
            limit=1000  # Adjust the limit if necessary
        )
        # Convert to DataFrame
        df = pd.DataFrame(response['records'])
        df['Model year'] = pd.to_numeric(df['Model year'], errors='coerce')
        df['Vehicle class'] = df['Vehicle class'].fillna('Unknown')
        return df

    # Load the data
    df = load_data(API_URL, DATASET_ID)

    # Group and pivot the data
    vehicle_class_sum = df.groupby(['Model year', 'Vehicle class']).size().reset_index(name='Total')
    pivot_df = vehicle_class_sum.pivot(index='Model year', columns='Vehicle class', values='Total').fillna(0)

    # Sidebar Filters
    st.sidebar.header("Filter Options")
    vehicle_classes = st.sidebar.multiselect("Select Vehicle Classes", options=pivot_df.columns, default=pivot_df.columns)

    # Filter data based on selected vehicle classes
    filtered_df = pivot_df[vehicle_classes]

    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 8))
    filtered_df.plot(kind='bar', stacked=True, colormap='tab10', ax=ax)

    # Add titles and labels
    ax.set_title('Summe der Fahrzeugklassen pro Jahr', fontsize=16)
    ax.set_xlabel('Baujahr', fontsize=12)
    ax.set_ylabel('Fahrzeuge gesamt', fontsize=12)
    ax.legend(title='Fahrzeugklasse', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Display the plot in Streamlit
    st.pyplot(fig)
