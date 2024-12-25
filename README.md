# Migration de données CSV vers MongoDB
## Introduction

Ce projet permet de migrer des données contenues dans un fichier CSV vers une base de données MongoDB. Le fichier CSV contient des informations sur des patients (nom, âge, diagnostic, etc.), et le script permet d'importer ces données dans une base de données MongoDB, tout en vérifiant l'intégrité des données avant et après l'importation.

---

## Prérequis

### Logiciels nécessaires :

- **Python 3.x** : Assurez-vous d'avoir Python installé sur votre machine.
- **MongoDB** : Une instance MongoDB doit être en fonctionnement localement ou sur un serveur distant.
- **Bibliothèques Python** : Vous devez installer certaines bibliothèques Python via `pip` avant d'exécuter le script.

### Installation des dépendances :

Pour installer les dépendances requises, vous pouvez utiliser la commande suivante :


pip install pymongo

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
