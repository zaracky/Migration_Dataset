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

```bash
pip install pymongo
