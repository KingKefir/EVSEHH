import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

# Load CSV files
fuel_data_liter1 = pd.read_csv("data\\benzin.csv")  # Replace with your file path
fuel_data_liter2 = pd.read_csv("data\\diesel.csv")  # Replace with your file path
fuel_data_kwh = pd.read_csv("data\\elektro.csv")  # Replace with your file path

# Add fuel type column
fuel_data_liter1['fuel_type'] = 'benzin'
fuel_data_liter2['fuel_type'] = 'diesel'

# Concatenate liter data
fuel_data_liter = pd.concat([fuel_data_liter1, fuel_data_liter2], ignore_index=True)

# Set default fuel costs
default_benzin_cost = 1.83  # €/L
default_diesel_cost = 1.73  # €/L
default_electricity_cost = 0.44  # €/kWh

# Sidebar for fuel cost inputs
st.sidebar.header("Fuel Costs")
benzin_cost = st.sidebar.number_input("Benzin cost (€/L)", value=default_benzin_cost)
diesel_cost = st.sidebar.number_input("Diesel cost (€/L)", value=default_diesel_cost)
electricity_cost = st.sidebar.number_input("Electricity cost (€/kWh)", value=default_electricity_cost)

# Dropdown menus for car models
st.title("Car Model Cost Calculator")
st.write("Select two car models to compare costs over distance")

car_model_liter = st.selectbox("Select a car model (Liter/100km)", fuel_data_liter.iloc[:,1].unique())
car_model_kwh = st.selectbox("Select a car model (kWh/100km)", fuel_data_kwh['Modell'].unique())

# Distance input slider
distance = st.slider("Select the distance (km)", min_value=1, max_value=1000, value=100, step=10)

# Function to calculate costs
def calculate_cost(model, fuel_type, consumption, distance, fuel_cost):
    return (consumption / 100) * distance * fuel_cost

# Get data and calculate costs
if car_model_liter:
    car_data_liter = fuel_data_liter[fuel_data_liter.iloc[:,1] == car_model_liter].iloc[0]
    fuel_type_liter = car_data_liter['fuel_type']  # Assuming fuel type column is present (e.g., "benzin" or "diesel")
    consumption_liter = car_data_liter['l/100km']

    # Determine cost per fuel type
    fuel_cost_liter = benzin_cost if fuel_type_liter == "benzin" else diesel_cost
    cost_liter = calculate_cost(car_model_liter, fuel_type_liter, consumption_liter, distance, fuel_cost_liter)

if car_model_kwh:
    car_data_kwh = fuel_data_kwh[fuel_data_kwh['Modell'] == car_model_kwh].iloc[0]
    consumption_kwh = car_data_kwh['kWh/100km']
    cost_kwh = calculate_cost(car_model_kwh, "electricity", consumption_kwh, distance, electricity_cost)

# Plotting
fig, ax = plt.subplots()
ax.plot([0, distance], [0, cost_liter], label=f"{car_model_liter} ({fuel_type_liter}) - €{fuel_cost_liter:.2f}/L")
ax.plot([0, distance], [0, cost_kwh], label=f"{car_model_kwh} (electricity) - €{electricity_cost:.2f}/kWh")
ax.set_xlabel("Distance (km)")
ax.set_ylabel("Cost (€)")
ax.legend()
st.pyplot(fig)
