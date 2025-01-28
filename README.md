# Migration de données CSV vers MongoDB

## Table des matières


1. [Fonctionnement et utilité du programme](#fonctionnement-et-utilité-du-programme)
2. [Déploiement et exécution](#déploiement-et-exécution)
4. [Système d'authentification et rôles utilisateurs](#système-dauthentification-et-rôles-utilisateurs)
5. [Schéma de la base de données](#schéma-de-la-base-de-données)
6. [Structure du projet](#structure-du-projet)
   
## Introduction

Ce projet permet d'importer des données depuis un fichier CSV dans une base de données MongoDB en utilisant des conteneurs Docker. Le processus de migration comprend plusieurs étapes clés : le nettoyage et la transformation des données, l'importation en lots dans MongoDB, et la gestion de différents rôles utilisateurs avec des permissions spécifiques.

Ce document décrit la logique de migration, le déploiement du programme, le système d'authentification et les rôles utilisateurs, ainsi que le schéma de la base de données.

---
## Fonctionnement et utilité du programme

Le programme vise à automatiser l'importation de données depuis un fichier CSV dans une base de données MongoDB. L'objectif principal est de permettre à l'utilisateur de charger des informations structurées (comme celles d'une clinique ou d'un hôpital) dans MongoDB avec un nettoyage et une validation des données.

### Processus principal :

1. **Chargement des données CSV** : Le fichier CSV est lu ligne par ligne.
2. **Transformation des données** : Les données sont vérifiées et converties dans des types compatibles avec MongoDB (par exemple, conversion des âges en entiers, des montants de facturation en flottants, etc.).
3. **Vérification des doublons** : Avant d'insérer chaque ligne, le programme vérifie si un document avec des données similaires existe déjà dans la base de données pour éviter les doublons.
4. **Insertion dans MongoDB** : Les données validées sont insérées dans la base de données MongoDB en utilisant des insertions par lots pour optimiser les performances.
5. **Création d'index** : Après l'insertion, des index sont créés sur certains champs clés comme "Nom", "Numéro de chambre", et "Date d'admission" pour accélérer les recherches.
6. **Logging des opérations** : Le processus utilise un système de logging pour suivre l'état des différentes étapes du programme (chargement des données, vérification des doublons, insertions réussies ou échouées, erreurs de transformation de données, etc.). Cela permet à l'utilisateur de suivre l'avancement de l'importation et de diagnostiquer les erreurs de manière plus efficace.

### Utilité pour l'utilisateur

- **Gain de temps** : L'automatisation de l'importation et de la validation des données permet de réduire les erreurs humaines et d'éviter des processus manuels longs.
- **Validité des données** : Le programme effectue des vérifications et conversions de données pour s'assurer qu'elles sont conformes aux attentes avant de les insérer dans la base de données.
- **Évolutivité** : Il peut traiter de grandes quantités de données sans compromettre la performance, en utilisant des insertions par lots et des vérifications de doublons.




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

`MONGO_INITDB_ROOT_USERNAME=admin`

`MONGO_INITDB_ROOT_PASSWORD=adminpassword`

`MONGO_HOST=mongodb`

`MONGO_PORT=27017`

`DATABASE_NAME=entreprise`

`COLLECTION_NAME=employes`

3. Installez les dépendances :

`pip install -r requirements.txt`

4.Vérifiez votre instance MongoDB : 
Assurez-vous que MongoDB fonctionne et que vous pouvez vous connecter avec les informations fournies dans le fichier .env. Si vous utilisez Docker pour MongoDB, assurez-vous que le conteneur est en cours d'exécution:

`docker-compose up --build `
## Exécution du script
Une fois que vous avez configuré l'environnement, vous pouvez exécuter le script principal (script.py) avec la commande suivante :

`python script.py`

Le script va :

- Se connecter à MongoDB avec les informations contenues dans le fichier .env.

- Charger les données du fichier CSV spécifié (healthcare_dataset.csv).

- Transformer et valider les données.

- Insérer les données dans MongoDB (par lots de 1000 documents).

- Créer des index pour améliorer les performances de recherche sur certains champs.

- Logger les étapes du processus (insertion, vérification des doublons, erreurs, etc.).


### Logs

Les logs seront enregistrés dans un fichier nommé data_migration.log. Vous pouvez consulter ce fichier pour vérifier l'état de l'importation et résoudre tout problème potentiel.

Si vous souhaitez exécuter ce script automatiquement dans un environnement Docker, vous pouvez également utiliser le fichier `docker-compose.yml` pour démarrer les services nécessaires, notamment MongoDB et votre application Python.


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

