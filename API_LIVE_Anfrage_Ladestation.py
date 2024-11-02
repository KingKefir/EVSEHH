import requests

# Basis-URL und Feature-ID (ersetzen Sie {featureId} durch die gewünschte ID)
base_url = "https://api.hamburg.de/datasets/v1/emobility/collections/stromnetz_emobility/items"
feature_id = "8554580"  # Beispiel Feature-ID

# Erstellen der vollständigen URL mit der Feature-ID
url = f"{base_url}/{feature_id}"

# Optionale Parameter
params = {
    "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84",  # Standard-Koordinatenreferenzsystem
    "f": "json",  # Format der Antwort
    "properties": "standort,adresse,anzahl_ladepunkte,typ,stecker,status,ladesaeule_status"  # Ausgewählte Eigenschaften, einschließlich aktueller Status
}

# Header für die Anfrage (falls ein Token benötigt wird, können Sie es hier hinzufügen)
headers = {
    "Accept": "application/json",
    # "Authorization": "Bearer YOUR_ACCESS_TOKEN"  # Optional: Token, falls erforderlich
}

# Anfrage an die API senden
response = requests.get(url, headers=headers, params=params)

# Überprüfung und Verarbeitung der Antwort
if response.status_code == 200:
    data = response.json()  # Antwort in JSON konvertieren
    print("Feature Data:")
    print(f"Standort: {data['properties'].get('standort', 'Nicht verfügbar')}")
    print(f"Adresse: {data['properties'].get('adresse', 'Nicht verfügbar')}")
    print(f"Anzahl Ladepunkte: {data['properties'].get('anzahl_ladepunkte', 'Nicht verfügbar')}")
    print(f"Typ: {data['properties'].get('typ', 'Nicht verfügbar')}")
    print(f"Stecker: {data['properties'].get('stecker', 'Nicht verfügbar')}")
    print(f"Status: {data['properties'].get('status', 'Nicht verfügbar')}")
    print(f"Ladesäule Status: {data['properties'].get('ladesaeule_status', 'Nicht verfügbar')}")
else:
    print("Fehler:", response.status_code, response.text)