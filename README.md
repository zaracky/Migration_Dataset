# Migration de données CSV vers MongoDB

## Table des matières

1. [Logique de la migration](#logique-de-la-migration)
2. [Déploiement et exécution](#déploiement-et-exécution)
3. [Système d'authentification et rôles utilisateurs](#système-dauthentification-et-rôles-utilisateurs)
4. [Schéma de la base de données](#schéma-de-la-base-de-données)
5. [Structure du projet](#structure-du-projet)
   
## Introduction

Ce projet permet d'importer des données depuis un fichier CSV dans une base de données MongoDB en utilisant des conteneurs Docker. Le processus de migration comprend plusieurs étapes clés : le nettoyage et la transformation des données, l'importation en lots dans MongoDB, et la gestion de différents rôles utilisateurs avec des permissions spécifiques.

Ce document décrit la logique de migration, le déploiement du programme, le système d'authentification et les rôles utilisateurs, ainsi que le schéma de la base de données.

---
## Logique de la migration

La logique de la migration est divisée en plusieurs étapes, qui permettent de convertir les données du fichier CSV en documents MongoDB valides...

## Déploiement et exécution

## Prérequis

### Logiciels nécessaires :

- **Python 3.x** : Assurez-vous d'avoir Python installé sur votre machine.
- **MongoDB** : Une instance MongoDB doit être en fonctionnement localement ou sur un serveur distant.
- **Bibliothèques Python** : Vous devez installer certaines bibliothèques Python via `pip` avant d'exécuter le script.
- **Docker** : Vous devez avoir Docker installé pour pouvoir exécuter les conteneurs nécessaires...


### Installation :
1. Clonez ce dépôt sur votre machine locale :
`git clone https://github.com/zaracky/Migration_Dataset.git`

2.Créez un fichier .env dans le répertoire racine du projet et ajoutez vos informations de connexion MongoDB ainsi que les paramètres de la base de données. Voici un exemple de contenu pour votre fichier .env :

MONGO_INITDB_ROOT_USERNAME=admin

MONGO_INITDB_ROOT_PASSWORD=adminpassword

MONGO_HOST=mongodb

MONGO_PORT=27017

DATABASE_NAME=entreprise

COLLECTION_NAME=employes

3. Installez les dépendances :

`pip install -r requirements.txt`

4. Construisez et lancez les conteneurs Docker :
`docker-compose up --build `

5. Une fois le programme lancé, le script commencera à importer les données depuis le fichier CSV vers la base de données MongoDB.

## Fonctionnement et utilité du programme

Le programme vise à automatiser l'importation de données depuis un fichier CSV dans une base de données MongoDB. L'objectif principal est de permettre à l'utilisateur de charger des informations structurées (comme celles d'une clinique ou d'un hôpital) dans MongoDB avec un nettoyage et une validation des données.

### Processus principal :

1. **Chargement des données CSV** : Le fichier CSV est lu ligne par ligne.
2. **Transformation des données** : Les données sont vérifiées et converties dans des types compatibles avec MongoDB (par exemple, conversion des âges en entiers, des montants de facturation en flottants, etc.).
3. **Vérification des doublons** : Avant d'insérer chaque ligne, le programme vérifie si un document avec des données similaires existe déjà dans la base de données pour éviter les doublons.
4. **Insertion dans MongoDB** : Les données validées sont insérées dans la base de données MongoDB en utilisant des insertions par lots pour optimiser les performances.
5. **Création d'index** : Après l'insertion, des index sont créés sur certains champs clés comme "Nom", "Numéro de chambre", et "Date d'admission" pour accélérer les recherches.

Le programme est particulièrement utile pour les environnements où les données évoluent fréquemment et où il est nécessaire d'importer de grandes quantités de données sans perte de performance.

### Utilité pour l'utilisateur

- **Gain de temps** : L'automatisation de l'importation et de la validation des données permet de réduire les erreurs humaines et d'éviter des processus manuels longs.
- **Validité des données** : Le programme effectue des vérifications et conversions de données pour s'assurer qu'elles sont conformes aux attentes avant de les insérer dans la base de données.
- **Évolutivité** : Il peut traiter de grandes quantités de données sans compromettre la performance, en utilisant des insertions par lots et des vérifications de doublons.

- 

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

## Système d'authentification et rôles utilisateurs
Le système d'authentification dans ce projet repose sur la création de plusieurs utilisateurs avec différents rôles. Ces utilisateurs ont accès à la base de données MongoDB avec des privilèges spécifiques :

### Utilisateurs et rôles
#### Admin (dbOwner) :
Accès complet à la base de données.
Peut créer, modifier et supprimer des données ainsi que gérer les utilisateurs.

#### Devs (readWrite) :
Accès en lecture et écriture à la base de données.
Peut manipuler les documents dans la base de données.

#### Consultant (read) :
Accès en lecture uniquement.
Ne peut pas modifier les données, mais peut consulter les informations dans la base de données.

### Création des utilisateurs
Les utilisateurs sont créés au moment de l'initialisation de MongoDB via un script init-mongo.js. Ce script crée les utilisateurs avec les informations définies dans le fichier .env.

## Schéma de la base de données
La base de données MongoDB utilisée dans ce projet est structurée autour d'une collection principale qui contient les informations des patients.

Voici un schéma simplifié de la structure de la base de données :


Collection patients : Contient les informations de chaque patient.
Name : Nom du patient (string).
Age : Âge du patient (int).
Gender : Genre (string, peut être "Male" ou "Female").
Blood Type : Groupe sanguin (string).
Medical Condition : Condition médicale (string).
Date of Admission : Date d'admission (Date).
Room Number : Numéro de chambre (int).
Billing Amount : Montant de la facturation (float).

## Structure du projet

Voici la structure des fichiers du projet :
project/
│

├── docker-compose.yml        # Configuration des services Docker

├── init-mongo.js             # Script d'initialisation de MongoDB

├── requirements.txt          # Liste des dépendances Python

├── script.py                 # Script Python d'importation des données

├── healthcare_dataset.csv    # Fichier CSV des données à importer

├── images/                   # Dossier contenant les schémas et diagrammes

│   └── database_schema.png   # Schéma de la base de données

└── README.md                 # Documentation du projet




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

