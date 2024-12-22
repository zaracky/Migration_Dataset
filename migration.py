import csv
from pymongo import MongoClient

# Configuration MongoDB
MONGO_URI = "**mongodb://localhost:27017**"  # URL de connexion MongoDB (adapter si nécessaire)
DATABASE_NAME = "**ma_base_de_donnees**"     # Nom de la base de données
COLLECTION_NAME = "**ma_collection**"        # Nom de la collection

CSV_FILE_PATH = "**chemin/vers/votre_fichier.csv**"  # Chemin du fichier CSV

# Connexion à MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    print("Connexion à MongoDB réussie.")
except Exception as e:
    print(f"Erreur de connexion à MongoDB : {e}")
    exit()

# Lecture du fichier CSV et insertion dans MongoDB
try:
    with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)  # Lecture en tant que dictionnaire (colonnes = clés)
        
        # Conversion des lignes CSV en documents MongoDB
        documents = []
        for row in reader:
            # Adapter si une transformation spécifique est nécessaire (ex. convertir en entier)
            # row['age'] = int(row['age'])  # Exemple : conversion en entier
            documents.append(row)
        
        # Insertion en lot
        if documents:
            result = collection.insert_many(documents)
            print(f"{len(result.inserted_ids)} documents insérés avec succès dans MongoDB.")
        else:
            print("Le fichier CSV est vide ou mal formaté.")
except FileNotFoundError:
    print(f"Le fichier CSV '{CSV_FILE_PATH}' est introuvable.")
except Exception as e:
    print(f"Erreur lors de l'importation des données : {e}")
finally:
    client.close()
