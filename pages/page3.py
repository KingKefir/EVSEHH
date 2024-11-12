import pandas as pd

# Load the three CSV files
fuel_data_benzin = pd.read_csv("data\\benzin.csv")  # Replace with the actual file path
fuel_data_diesel = pd.read_csv("data\\diesel.csv")  # Replace with the actual file path
fuel_data_electric = pd.read_csv("data\\elektro.csv")  # Replace with the actual file path

# Add fuel type and unit columns to each DataFrame
fuel_data_benzin['fuel_type'] = 'benzin'
fuel_data_benzin['unit'] = 'liter'
fuel_data_diesel['fuel_type'] = 'diesel'
fuel_data_diesel['unit'] = 'liter'
fuel_data_electric['fuel_type'] = 'electricity'
fuel_data_electric['unit'] = 'kWh'

# Standardize column names to match across all files
fuel_data_benzin.rename(columns={'l/100km': 'consumption_per_100km'}, inplace=True)
fuel_data_diesel.rename(columns={'l/100km': 'consumption_per_100km'}, inplace=True)
fuel_data_electric.rename(columns={'kWh/1ookm': 'consumption_per_100km'}, inplace=True)

# Concatenate the DataFrames
combined_data = pd.concat([fuel_data_benzin, fuel_data_diesel, fuel_data_electric], ignore_index=True)

# Save the combined DataFrame to a new CSV file
combined_data.to_csv("data\\combined_car_fuel_data.csv", index=False)

print("Combined data saved to 'combined_car_fuel_data.csv'")
