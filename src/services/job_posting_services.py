import requests
import logging
import datetime
from helpers.access_token import get_access_token 

# Configuration de la journalisation
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Constantes et configuration
API_URL = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"

# Fonction d'assistance pour effectuer les requêtes à l'API
def fetch_job_postings(params):
    # Obtient le jeton d'accès (access token) pour authentification
    token = get_access_token()
    if not token:
        logger.error("Échec de récupération du jeton d'accès.")
        return None

    # Prépare les en-têtes de la requête avec le jeton d'authentification
    headers = {
        "Authorization": f"Bearer {token}",
    }
    
    try:
        # Effectue la requête GET à l'API avec les paramètres spécifiés
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()  # Génère une erreur HTTP si la réponse est invalide (codes 4xx ou 5xx)
        
        # Vérifie si le statut de la réponse est 200 (succès) ou 206 (succès partiel)
        if response.status_code in [200, 206]:
            raw_data = response.json()
            
            job_postings = []
            # Parcourt chaque résultat pour extraire les informations de l'offre d'emploi
            for result in raw_data.get("resultats", []):
                job_posting = {
                    "title": result.get("intitule"),
                    "company": result.get("entreprise", {}).get("nom"),
                    "location": result.get("lieuTravail", {}).get("libelle"),
                    "postal_code": result.get("lieuTravail", {}).get("codePostal"),
                    "contract_type": result.get("typeContratLibelle"),
                    "description": result.get("description"),
                    "salary": result.get("salaire", {}).get("libelle"),
                    "required_experience": result.get("experienceLibelle"),
                    "qualifications": [comp.get("libelle") for comp in result.get("competences", [])],
                    "date_created": result.get("dateCreation"),
                    "application_url": result.get("contact", {}).get("urlPostulation"),
                    "department": result.get("lieuTravail", {}).get("codePostal", "")[:2],  # Utilise les 2 premiers chiffres comme code départemental
                    "commune": result.get("lieuTravail", {}).get("commune"),
                    "domain": result.get("domaine"),
                    "region": result.get("region")
                }
                job_postings.append(job_posting)
                
            return job_postings
        else:
            logger.error(f"Code de statut inattendu {response.status_code}")
            logger.debug(f"Contenu de la réponse: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Échec de la requête: {str(e)}")
        return None

# Fonction pour obtenir les offres d'emploi du jour
def get_daily_postings():
    today = datetime.date.today()
    params = {
        "minCreationDate": today.strftime("%Y-%m-%dT00:00:00Z"),
        "maxCreationDate": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": "0-9"
    }
    return fetch_job_postings(params)

# Fonction pour récupérer les offres d'emploi sur une période définie, sans générer de statistiques
def fetch_historical_postings(start_date, end_date, step_days=7):
    postings = []  # Stocke toutes les offres d'emploi
    current_date = start_date

    # Boucle à travers les intervalles de dates jusqu'à la date de fin
    while current_date <= end_date:
        next_date = min(current_date + datetime.timedelta(days=step_days), end_date)
        params = {
            "minCreationDate": current_date.strftime("%Y-%m-%dT00:00:00Z"),
            "maxCreationDate": next_date.strftime("%Y-%m-%dT23:59:59Z"),
            "range": "0-9",
        }
        
        logger.debug(f"Requête des offres d'emploi avec les paramètres: {params}")

        try:
            data = fetch_job_postings(params)
            if data:
                postings.extend(data)
                logger.debug(f"Récupéré {len(data)} offres d'emploi de {current_date} à {next_date}")
            else:
                logger.warning(f"Aucune offre trouvée de {current_date} à {next_date}")
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des offres pour la période {current_date} à {next_date}: {str(e)}")
            return None, None  # Renvoie None si une erreur survient

        current_date = next_date + datetime.timedelta(days=1)

    return postings, {}  # Retourne temporairement un dictionnaire vide pour le suivi des statistiques
