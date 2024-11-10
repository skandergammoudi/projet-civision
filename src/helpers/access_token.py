import os
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def get_access_token():
    """
    Récupère le jeton d'accès depuis l'API France Travail en utilisant les identifiants client.

    Retourne:
    - str: Le jeton d'accès pour les requêtes API.
    - None: Si la requête échoue.
    """
    # Obtenir les identifiants depuis les variables d'environnement
    client_id = os.getenv("FRANCE_TRAVAIL_CLIENT_ID")
    client_secret = os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET")
    scope = os.getenv("FRANCE_TRAVAIL_SCOPE")

    # Vérifier si les identifiants sont bien chargés
    if not client_id or not client_secret or not scope:
        print("Erreur : Variables d'environnement manquantes pour client_id, client_secret, ou scope.")
        return None

    # URL pour obtenir le jeton d'accès
    token_url = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"

    # En-têtes et données pour la requête
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope
    }

    # Envoyer la requête POST pour obtenir le jeton
    response = requests.post(token_url, headers=headers, data=data)

    if response.status_code == 200:
        # Récupération réussie du jeton
        token_data = response.json()
        access_token = token_data.get("access_token")
        print("Jeton d'accès récupéré :", access_token)  # Pour vérifier le jeton
        return access_token
    else:
        # Gestion des erreurs
        print(f"Erreur lors de l'obtention du jeton d'accès : {response.status_code}")
        print(response.json())
        return None
