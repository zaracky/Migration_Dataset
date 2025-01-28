# Migration de données CSV vers MongoDB
## Introduction

Ce projet permet de migrer des données contenues dans un fichier CSV vers une base de données MongoDB. Le fichier CSV contient des informations sur des patients (nom, âge, diagnostic, etc.), et le script permet d'importer ces données dans une base de données MongoDB, tout en vérifiant l'intégrité des données avant et après l'importation.

---

## Prérequis

### Logiciels nécessaires :

- **Python 3.x** : Assurez-vous d'avoir Python installé sur votre machine.
- **MongoDB** : Une instance MongoDB doit être en fonctionnement localement ou sur un serveur distant.
- **Bibliothèques Python** : Vous devez installer certaines bibliothèques Python via `pip` avant d'exécuter le script.

### Installation :
1. Clonez ce dépôt sur votre machine locale :
git clone https://github.com/zaracky/Migration_Dataset.git

2.Créez un fichier .env dans le répertoire racine du projet et ajoutez vos informations de connexion MongoDB ainsi que les paramètres de la base de données. Voici un exemple de contenu pour votre fichier .env :
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=adminpassword
MONGO_HOST=mongodb
MONGO_PORT=27017
DATABASE_NAME=entreprise
COLLECTION_NAME=employes

## Fonctionnement du script

Le script suit les étapes suivantes :

### 1. Connexion à MongoDB

Le script se connecte à une instance de MongoDB à l'adresse `localhost` (ou une autre adresse si nécessaire) et accède à une base de données et une collection spécifiques. Dans le code, la base de données utilisée est `entreprise` et la collection est `employes`. Voici un extrait de code de cette connexion :
client = MongoClient("mongodb://localhost:27017")
db = client["entreprise"]  # Nom de la base de données
collection = db["employes"]  # Nom de la collection

### 2. Importation des données depuis un CSV
Le script lit un fichier CSV contenant les données et les transforme pour correspondre aux types attendus (par exemple, les valeurs numériques sont converties en int ou float).

### 3. Insertion dans MongoDB
Les données sont insérées dans MongoDB par lots pour éviter les problèmes liés à l'insertion de grandes quantités de données. Cela permet d'optimiser les performances du processus.

### 4. Vérification de l'intégrité des données :
Vérification que toutes les colonnes attendues sont présentes.
Vérification des doublons dans les données.
Vérification de la validité des types de données (par exemple, s'assurer que l'âge est un nombre entier).
Recherche des valeurs manquantes dans les documents insérés.
### 5. Journalisation (Logging)
Le processus est entièrement journalisé pour permettre de suivre l'avancement et de repérer les erreurs éventuelles. Un fichier data_migration.log est créé pour conserver l'historique des actions.

## Comment exécuter le script
Assurez-vous que MongoDB est en cours d'exécution et accessible via l'URI spécifié dans votre fichier .env.
Lancez le script Python pour importer les données depuis le fichier CSV dans la base de données MongoDB :

python script.py

Le script procédera à la transformation des données du fichier CSV, à la vérification des doublons et à l'insertion dans la collection MongoDB. Les logs de l'exécution seront enregistrés dans le fichier data_migration.log.

## Fonctionnalités du script
Transformation des données : Le script nettoie et transforme certaines colonnes du CSV (par exemple, la conversion des âges en entiers, le montant de facturation en flottants).

Création des utilisateurs MongoDB : Les utilisateurs sont créés automatiquement avec les rôles appropriés (consultant, devs, admin) en fonction des paramètres dans le fichier .env.

Insertion des données : Les données sont insérées dans la base de données MongoDB en lots (1000 documents par lot).

Vérification de l'intégrité des données : Le script vérifie l'intégrité des données importées (absence de doublons et types corrects pour certaines colonnes).

## Indexation
Après l'importation des données, le script crée des index sur les colonnes suivantes :
Name
Room Number
Date of Admission
Cela permet d'améliorer les performances des recherches sur ces champs.

## Gestion des logs
Le script génère un fichier de log appelé data_migration.log dans le répertoire courant. Ce fichier contient toutes les informations sur l'exécution du script, y compris :
Le nombre de documents insérés.
Les erreurs de type de données ou de doublons rencontrées pendant l'importation.
Les problèmes d'intégrité détectés dans les données.

