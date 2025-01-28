import csv
import logging
from pymongo import MongoClient, errors
from datetime import datetime

# Configuration du journal de log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("data_migration.log"),  # Fichier log
        logging.StreamHandler()  # Affichage console
    ]
)

# Fonction pour nettoyer et transformer les types de données
def transform_row(row):
    """
    Transforme les types de données dans une ligne du fichier CSV.
    """
    try:
        # Convertir la colonne 'Age' en entier
        if "Age" in row and row["Age"].strip().isdigit():
            row["Age"] = int(row["Age"].strip())  # Convertir Age en entier
        else:
            logging.error(f"Valeur invalide pour 'Age' : {row['Age']} dans la ligne {row}")

        # Convertir la colonne 'Billing Amount' en flottant
        if "Billing Amount" in row:
            try:
                row["Billing Amount"] = float(row["Billing Amount"].strip())  # Convertir Billing Amount en flottant
            except ValueError:
                logging.error(f"Valeur invalide pour 'Billing Amount' : {row['Billing Amount']} dans la ligne {row}")
        
        # Convertir la colonne 'Room Number' en entier
        if "Room Number" in row and row["Room Number"].strip().isdigit():
            row["Room Number"] = int(row["Room Number"].strip())  # Convertir Room Number en entier
        else:
            logging.error(f"Valeur invalide pour 'Room Number' : {row['Room Number']} dans la ligne {row}")

        # Vérification du genre (Male ou Female)
        if "Gender" in row and row["Gender"].strip() not in ["Male", "Female"]:
            logging.error(f"Valeur invalide pour 'Gender' : {row['Gender']} dans la ligne {row}")
        
        # Vérification du groupe sanguin
        if "Blood Type" in row and row["Blood Type"].strip() not in ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]:
            logging.error(f"Valeur invalide pour 'Blood Type' : {row['Blood Type']} dans la ligne {row}")

        # Vérification de la condition médicale
        if "Medical Condition" in row and not row["Medical Condition"].strip():
            logging.error(f"Valeur manquante pour 'Medical Condition' dans la ligne {row}")

        # Vérification de la date d'admission au format attendu
        if "Date of Admission" in row:
            try:
                row["Date of Admission"] = datetime.strptime(row["Date of Admission"], "%Y-%m-%d")  # Convertir la date
            except ValueError:
                logging.error(f"Valeur invalide pour 'Date of Admission' : {row['Date of Admission']} dans la ligne {row}")

    except ValueError as e:
        logging.error(f"Erreur de conversion des types dans la ligne : {row}. Erreur : {e}")
    return row

# Connexion à MongoDB
def connect_to_mongodb(uri="mongodb://admin:adminpassword@mongodb:27017", db_name="entreprise", collection_name="employes"):

    try:
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        logging.info(f"Connexion réussie à MongoDB : {uri}, Base : {db_name}, Collection : {collection_name}")
        return collection
    except errors.ConnectionError as e:
        logging.error(f"Erreur de connexion à MongoDB : {e}")
        raise

# Création d'index sur les champs pertinents
def create_indexes(collection):
    try:
        # Index sur le nom
        collection.create_index([("Name", 1)])
        logging.info("Index créé sur 'Name'.")

        # Index sur le numéro de chambre
        collection.create_index([("Room Number", 1)])
        logging.info("Index créé sur 'Room Number'.")

        # Index sur la date d'admission
        collection.create_index([("Date of Admission", 1)])
        logging.info("Index créé sur 'Date of Admission'.")
        
    except Exception as e:
        logging.error(f"Erreur lors de la création des index : {e}")


# Importation des données CSV avec insertion par lots
def import_csv_to_mongodb(csv_file_path, collection, batch_size=1000):
    try:
        with open(csv_file_path, mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            batch = []
            count = 0
            duplicates = 0
            
            for row in reader:
                row = transform_row(row)  # Transformer les types avant insertion
                batch.append(row)
                count += 1
                
                # Vérification des doublons
                if collection.find_one({"Name": row["Name"], "Room Number": row["Room Number"], "Date of Admission": row["Date of Admission"]}):
                    logging.warning(f"Doublon détecté pour {row['Name']} (Room: {row['Room Number']}, Admission Date: {row['Date of Admission']}). Ce document ne sera pas importé.")
                    duplicates += 1
                    continue  # Ne pas insérer ce doublon dans la base de données
                
                if len(batch) == batch_size:
                    collection.insert_many(batch, ordered=False)
                    logging.info(f"{len(batch)} documents insérés.")
                    batch = []
            
            if batch:
                collection.insert_many(batch, ordered=False)
                logging.info(f"{len(batch)} documents restants insérés.")
            
            logging.info(f"Importation terminée : {count} lignes insérées au total.")
            if duplicates > 0:
                logging.warning(f"{duplicates} doublons ont été ignorés.")
    except FileNotFoundError:
        logging.error(f"Fichier CSV introuvable : {csv_file_path}")
        raise
    except errors.BulkWriteError as bwe:
        logging.error(f"Erreur lors de l'insertion en lot : {bwe.details}")


# Test d'intégrité des données
def test_data_integrity(collection):
    logging.info("Début des tests d'intégrité...")
    success = True

    # Liste des colonnes attendues
    expected_columns = [
        "Name", "Age", "Gender", "Blood Type", "Medical Condition", "Date of Admission",
        "Doctor", "Hospital", "Insurance Provider", "Billing Amount", "Room Number",
        "Admission Type", "Discharge Date", "Medication", "Test Results"
    ]

  # Vérification des colonnes
    for doc in collection.find():
        for col in expected_columns:
            if col not in doc:
                logging.error(f"Colonne manquante : {col} dans le document {doc}")
                success = False
            elif col == "Age" and not isinstance(doc.get(col), (int, float)):
                logging.error(f"Type incorrect pour la colonne {col} dans le document {doc}")
                success = False
            elif col == "Billing Amount" and not isinstance(doc.get(col), (int, float)):
                logging.error(f"Type incorrect pour la colonne {col} dans le document {doc}")
                success = False
            elif col == "Room Number" and not isinstance(doc.get(col), int):
                logging.error(f"Type incorrect pour la colonne {col} dans le document {doc}")
                success = False
            elif col == "Date of Admission" and not isinstance(doc.get(col), datetime):
                logging.error(f"Type incorrect pour la colonne {col} dans le document {doc}")
                success = False

    # Vérification des doublons sur la combinaison des champs "Name", "Room Number" et "Date of Admission"
    pipeline = [
        {"$group": {"_id": {"Name": "$Name", "Room Number": "$Room Number", "Date of Admission": "$Date of Admission"}, "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    duplicates = list(collection.aggregate(pipeline))
    if duplicates:
        for dup in duplicates:
            logging.error(f"Doublon trouvé : {dup['_id']} (Occurrences : {dup['count']})")
        success = False

    # Vérification des valeurs manquantes
    for doc in collection.find():
        for key, value in doc.items():
            if value in [None, ""]:
                logging.error(f"Valeur manquante pour '{key}' dans le document {doc}")
                success = False

    if success:
        logging.info("Tous les tests d'intégrité ont réussi.")
    else:
        logging.warning("Certains tests d'intégrité ont échoué.")

# Fonction principale
def main():
    csv_file_path = r"/usr/src/app/healthcare_dataset.csv"  # Chemin vers le fichier CSV
    collection = connect_to_mongodb()

    # Importation des données
    import_csv_to_mongodb(csv_file_path, collection)

    # Créer les index après l'importation
    create_indexes(collection)

    # Test d'intégrité après importation
    test_data_integrity(collection)

if __name__ == "__main__":
    main()
