import csv
from pymongo import MongoClient
from pymongo import MongoClient, errors

# Configuration du journal de log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("data_migration.log"),  # Fichier log
        logging.StreamHandler()  # Affichage console
    ]
)


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


def test_integrity(collection):
    print("Début des tests d'intégrité...")
    
    # Vérification des colonnes
    columns = ["Name","Age","Gender","Blood Type","Medical Condition","Date of Admission","Doctor","Hospital","Insurance Provider","Billing Amount","Room Number","Admission Type","Discharge Date","Medication","Test Results"]
    documents = collection.find()
    for doc in documents:
        for col in columns:
            if col not in doc:
                print(f"Colonne manquante : {col}")
            elif col == "age" and not isinstance(doc[col], int):
                print(f"Type incorrect pour {col} : {type(doc[col])}")

    # Vérification des doublons
    pipeline = [
        {"$group": {"_id": "$nom", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    duplicates = collection.aggregate(pipeline)
    for dup in duplicates:
        print(f"Doublon trouvé : {dup['_id']}")
    
    # Vérification des valeurs manquantes
    documents = collection.find()
    for doc in documents:
        for key, value in doc.items():
            if value in [None, ""]:
                print(f"Valeur manquante pour {key} dans {doc}")
    
    print("Tests d'intégrité terminés.")
test_integrity(collection)
