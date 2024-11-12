import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st
from ckanapi import RemoteCKAN

def show():
    st.title("Page 8")
    st.write("This is Page 8.")

    # Streamlit app title and description
    # st.set_page_config(layout="wide")
    st.title("Electric Vehicle Time Series Analysis")
    st.write("""
    This application retrieves EV data from a CKAN API, processes it, and provides a time series analysis of range and energy consumption.
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
    make_filter = st.sidebar.multiselect("Select Make", options=df['Make'].unique(), default=df['Make'].unique())
    year_filter = st.sidebar.slider("Select Model Year", int(df['Model year'].min()), int(df['Model year'].max()), (int(df['Model year'].min()), int(df['Model year'].max())))
    class_filter = st.sidebar.multiselect("Select Vehicle Class", options=df['Vehicle class'].unique(), default=df['Vehicle class'].unique())

    # Apply filters to DataFrame
    filtered_df = df[(df['Make'].isin(make_filter)) &
                    (df['Model year'] >= year_filter[0]) &
                    (df['Model year'] <= year_filter[1]) &
                    (df['Vehicle class'].isin(class_filter))]

    # Range vs. Efficiency Plot
    st.header("Range vs Efficiency (kWh/100 km)")
    fig1 = px.scatter(filtered_df, x='Combined (kWh/100 km)', y='Range (km)',
                    color='Make', hover_data=['Model year', 'Model'],
                    labels={'Combined (kWh/100 km)': 'Combined Consumption (kWh/100 km)',
                            'Range (km)': 'Range (km)'},
                    title="Range vs Combined Consumption by Make")
    st.plotly_chart(fig1)

    # Motor Power by Year Plot
    st.header("Motor Power over Model Years")
    fig2 = px.line(filtered_df, x='Model year', y='Motor (kW)', color='Make',
                labels={'Model year': 'Model Year', 'Motor (kW)': 'Motor Power (kW)'},
                title="Motor Power over Model Years")
    st.plotly_chart(fig2)

    # Range Distribution by Vehicle Class
    st.header("Range Distribution by Vehicle Class")
    fig3 = px.box(filtered_df, x='Vehicle class', y='Range (km)', color='Vehicle class',
                labels={'Vehicle class': 'Vehicle Class', 'Range (km)': 'Range (km)'},
                title="Range Distribution by Vehicle Class")
    st.plotly_chart(fig3)
