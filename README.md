# Projet Civision

Ce projet, développé pour Civision, permet de récupérer des offres d’emploi pour les clients français via l’API France Travail et de les enregistrer dans une base de données. Les données récupérées sont également analysées pour fournir des statistiques globales sur le marché de l’emploi par département, type de contrat et commune.

## Table des Matières
- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Endpoints](#endpoints)
- [Structure du Projet](#structure-du-projet)
- [Gestion du Jeton d'Accès](#gestion-du-jeton-daccès)
- [Technologies Utilisées](#technologies-utilisées)
- [Licence](#licence)

---

## Fonctionnalités

- **Récupération quotidienne des offres d’emploi** : Les offres d’emploi sont récupérées et stockées dans la base de données.
- **Historique des offres d’emploi** : Permet de récupérer des offres sur une période spécifiée.
- **Statistiques des offres d’emploi** : Génère des statistiques d’emploi globales basées sur les départements, les types de contrat et les communes.

---

## Installation

### Prérequis
- Python 3.x
- Flask
- Flask-SQLAlchemy
- Requests
- Flask-Swagger (pour la documentation API)
- Dotenv (pour la gestion des variables d'environnement)

### Étapes d’installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/skandergammoudi/projet-civision
   cd projet-civision
Installez les dépendances :

bash
Copier le code
pip install -r requirements.txt
Configurez les variables d’environnement dans un fichier .env à la racine du projet :

bash
Copier le code
FRANCE_TRAVAIL_CLIENT_ID=<votre_client_id>
FRANCE_TRAVAIL_CLIENT_SECRET=<votre_client_secret>
FRANCE_TRAVAIL_SCOPE=<votre_scope>
Utilisation
Lancez l'application Flask :

bash
Copier le code
python app.py
Accédez à la documentation Swagger de l'API à l’adresse suivante : http://localhost:5000/apidocs/.

Endpoints
1. Récupération des offres d'emploi
GET /job-postings/daily : Récupère les offres d’emploi du jour.
GET /job-postings/historical : Récupère les offres d’emploi sur une période définie. Requiert les paramètres start_date et end_date au format YYYY-MM-DD.
2. Statistiques des offres d'emploi
GET /stats/jobs-by-department : Retourne le nombre d'offres par département.
GET /stats/contract-type-evolution : Retourne le nombre d'offres par type de contrat.
GET /stats/jobs-by-commune : Retourne le nombre d'offres par commune.
Structure du Projet
plaintext
Copier le code
projet-civision/
├── app.py                 # Fichier principal qui lance l'application Flask
├── fetch_daily_postings.py # Module pour récupérer les offres d'emploi
├── services/
│   ├── job_posting_services.py # Services pour les requêtes API
│   └── access_token.py         # Gestion du jeton d'accès pour l'API France Travail
├── instance/
│   └── jobs.db             # Base de données SQLite (générée automatiquement)
├── templates/              # Fichiers HTML pour Swagger
└── .env                    # Fichier pour les variables d'environnement
Gestion du Jeton d'Accès
Fonction get_access_token
Le fichier access_token.py contient la fonction get_access_token() pour récupérer un jeton d’accès. Cette fonction :

Charge les identifiants (client_id, client_secret, et scope) depuis le fichier .env.
Envoie une requête POST pour obtenir le jeton.
Retourne le jeton d’accès ou None en cas d’échec.
Exemple d’utilisation
La fonction get_access_token() est appelée chaque fois qu’une requête API vers France Travail est envoyée. Le jeton d’accès valide est automatiquement utilisé dans les en-têtes de chaque requête.

Technologies Utilisées
Flask : Pour créer l'API RESTful.
SQLAlchemy : Pour gérer la base de données SQLite.
Requests : Pour interagir avec l'API France Travail.
Dotenv : Pour charger les variables d'environnement.
Flask-Swagger : Pour documenter l’API.