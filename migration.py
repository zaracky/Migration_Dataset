import csv
from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017")

# Création de la base de données et de la collection
db = client["entreprise"]  # Nom de la base de données
collection = db["employes"]  # Nom de la collection

# Lecture du fichier CSV
csv_file_path = "C:/Users/Loic/Documents/healthcare_dataset.csv"
with open(csv_file_path, mode="r", encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        collection.insert_one(row)  # Insertion d'un document dans la collection

print("Données insérées avec succès.")

