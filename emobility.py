import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSV-Datei laden
df = pd.read_csv("app_stromnetz_emobility_EPSG_4326.csv", sep=';')

# Erste Zeilen anzeigen, um einen Überblick zu erhalten
print(df.head())

# Datentypen und fehlende Werte überprüfen
print(df.info())
print(df.isnull().sum())

# Beschreibende Statistik der numerischen Spalten
print(df.describe())

adresse = df[['adresse', 'koordinaten', 'ladepunkt', 'the_geom']]

print(adresse.sample(10))