import pandas as pd

# Load your data
file_path = 'data\ladesaeulenregister_Bundesnetzagentur_2024.csv'  # Replace with your CSV file path
data = pd.read_csv(file_path, sep=';', skiprows=10)

# Display the first few rows
print("First 5 rows:")
print(data.sample(2).T)

# Show data types and null values
print("\nData types and null values:")
print(data.info())

# Describe numerical columns for basic stats
print("\nStatistical summary of numerical columns:")
print(data.describe())

# Check for missing values
print("\nMissing values in each column:")
print(data.isnull().sum())

# Display unique values for each column (if the dataset is not too large)
print("\nUnique values in each column:")
for col in data.columns:
    print(f"{col}: {data[col].nunique()} unique values")


unique_betreiber = data['Betreiber'].unique()

# Display the unique values
print("Unique occurrences of 'Betreiber':")
print(unique_betreiber)

bundesland_counts = data['Bundesland'].value_counts()


# Display the counts for each "Bundesland"
print("Sum of each occurrence of 'Bundesland':")
print(bundesland_counts)

laender = data['Bundesland'].unique()

# ## Bevölkerung je Bundesland Zensus 2022, alpabethisch sortiert
bevoelkerung = [11167721, 13105221, 3632853, 2545159, 695758, 1832675, 6236933, 1576049, 7982947, 14964420, 4108555, 1011891, 4049967,
2150239, 2939283, 2118830]

print("-----------")

count = 0 

lades_per_cap = {}

print("Ladesäulen je 100k Einwohner \n")
for i,j  in zip(bundesland_counts, bevoelkerung):
    print(f'{laender[count]}:   {round((i/j)*100000, 2)}')
    lades_per_cap[laender[count]] = round((i/j)*100000, 2)
    count += 1