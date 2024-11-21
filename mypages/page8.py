import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st
from ckanapi import RemoteCKAN

def app():
    APP_TITLE = 'Reichweiten- und Effizienzanalyse'
    
    st.title(APP_TITLE)

    # Streamlit app title and description
    # st.set_page_config(layout="wide")
    st.title("Electric Vehicle Time Series Analysis")
    st.write("""
    Hier nutzen wir öffentliche Kanadische Daten welche mittel CKAN API zur Verfügung gestellt werden.
    """)
    # Configure CKAN API URL and Dataset ID
    API_URL = "https://open.canada.ca/data/en/"
    DATASET_ID = "026e45b4-eb63-451f-b34f-d9308ea3a3d9"

    @st.cache_data
    def load_data(api_url, dataset_id):
        """Fetch data from CKAN API and return as a DataFrame."""
        ckan = RemoteCKAN(api_url)
        response = ckan.action.datastore_search(resource_id=dataset_id, limit=1000)
        df = pd.DataFrame(response['records'])
        return df

    # Load data
    df = load_data(API_URL, DATASET_ID)

    # Convert columns to numeric where needed
    df['Model year'] = pd.to_numeric(df['Model year'], errors='coerce')
    df['Range (km)'] = pd.to_numeric(df['Range (km)'], errors='coerce')
    df['Combined (kWh/100 km)'] = pd.to_numeric(df['Combined (kWh/100 km)'], errors='coerce')
    df['Motor (kW)'] = pd.to_numeric(df['Motor (kW)'], errors='coerce')

    # Sidebar filters
    st.sidebar.header("Filter Options")
    make_filter = st.sidebar.multiselect("Marke auswählen", options=df['Make'].unique(), default=df['Make'].unique())
    year_filter = st.sidebar.slider("Baujahr der Modells auswählen", int(df['Model year'].min()), int(df['Model year'].max()), (int(df['Model year'].min()), int(df['Model year'].max())))

    # Apply filters to DataFrame
    filtered_df = df[(df['Make'].isin(make_filter)) &
                    (df['Model year'] >= year_filter[0]) &
                    (df['Model year'] <= year_filter[1])]

    # Range vs. Efficiency Plot
    st.header("Reichweite - Wirkungsgrad (kWh/100 km)")
    fig1 = px.scatter(filtered_df, x='Combined (kWh/100 km)', y='Range (km)',
                    color='Make', hover_data=['Model year', 'Model'],
                    labels={'Combined (kWh/100 km)': 'Combined Consumption (kWh/100 km)',
                            'Range (km)': 'Range (km)'},
                    title="Reichweite gegenüber Gesamtverbraucht je Marke")
    st.plotly_chart(fig1)


    # Range Distribution by Make
    st.header("Box Plot der Reichweite nach Hersteller")
    fig2 = px.box(filtered_df, x='Make', y='Range (km)', color='Make',
                labels={'Make': 'Make', 'Range (km)': 'Range (km)'},
                title="Range Distribution by Make")
    st.plotly_chart(fig2)