import os
from flask import Flask, jsonify, request
import logging
import datetime
from flask_sqlalchemy import SQLAlchemy
from services.job_posting_services import get_daily_postings, fetch_historical_postings
from sqlalchemy import func
from flasgger import Swagger, swag_from



app = Flask(__name__)
swagger = Swagger(app)


# Configuration de l'URI de la base de données avec un chemin absolu
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'jobs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données
db = SQLAlchemy(app)

# Définition du modèle pour les offres quotidiennes
class JobPosting(db.Model):
    __tablename__ = 'job_postings'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    company = db.Column(db.String(100))
    location = db.Column(db.String(100))
    postal_code = db.Column(db.String(10))
    contract_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    salary = db.Column(db.String(50))
    required_experience = db.Column(db.String(100))
    qualifications = db.Column(db.String(200))
    date_created = db.Column(db.Date)
    application_url = db.Column(db.String(200))
    department = db.Column(db.String(10))
    commune = db.Column(db.String(50))
    domain = db.Column(db.String(50))
    region = db.Column(db.String(50))

# Définition du modèle pour les offres historiques
class HistoricalJobPosting(db.Model):
    __tablename__ = 'historical_job_postings'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    company = db.Column(db.String(100))
    location = db.Column(db.String(100))
    postal_code = db.Column(db.String(10))
    contract_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    salary = db.Column(db.String(50))
    required_experience = db.Column(db.String(100))
    qualifications = db.Column(db.String(200))
    date_created = db.Column(db.Date)
    application_url = db.Column(db.String(200))
    department = db.Column(db.String(10))
    commune = db.Column(db.String(50))
    domain = db.Column(db.String(50))
    region = db.Column(db.String(50))

# Setup logging configuration
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Sauvegarde des offres dans les tables "job_postings" et "historical_job_postings"
def save_job_postings(postings):
    for post in postings:
        job = JobPosting(
            title=post['title'],
            company=post['company'],
            location=post['location'],
            postal_code=post['postal_code'],
            contract_type=post['contract_type'],
            description=post['description'],
            salary=post['salary'],
            required_experience=post['required_experience'],
            qualifications=",".join(post['qualifications']),
            date_created=datetime.datetime.strptime(post['date_created'], "%Y-%m-%dT%H:%M:%S.%fZ").date() if post['date_created'] else None,
            application_url=post['application_url'],
            department=post['department'],
            commune=post['commune'],
            domain=post['domain'],
            region=post['region']
        )
        db.session.add(job)
    db.session.commit()

def save_historical_job_postings(postings):
    for post in postings:
        job = HistoricalJobPosting(
            title=post['title'],
            company=post['company'],
            location=post['location'],
            postal_code=post['postal_code'],
            contract_type=post['contract_type'],
            description=post['description'],
            salary=post['salary'],
            required_experience=post['required_experience'],
            qualifications=",".join(post['qualifications']),
            date_created=datetime.datetime.strptime(post['date_created'], "%Y-%m-%dT%H:%M:%S.%fZ").date() if post['date_created'] else None,
            application_url=post['application_url'],
            department=post['department'],
            commune=post['commune'],
            domain=post['domain'],
            region=post['region']
        )
        db.session.add(job)
    db.session.commit()

# Fonction pour sauvegarder les offres dans la table "historical_job_postings"
def save_historical_job_postings(postings):
    for post in postings:
        job = HistoricalJobPosting(
            title=post['title'],
            company=post['company'],
            location=post['location'],
            postal_code=post['postal_code'],
            contract_type=post['contract_type'],
            description=post['description'],
            salary=post['salary'],
            required_experience=post['required_experience'],
            qualifications=",".join(post['qualifications']),
            date_created=datetime.datetime.strptime(post['date_created'], "%Y-%m-%dT%H:%M:%S.%fZ").date() if post['date_created'] else None,
            application_url=post['application_url'],
            department=post['department'],
            commune=post['commune'],
            domain=post['domain'],
            region=post['region']
        )
        db.session.add(job)
    db.session.commit()


@app.route('/job-postings/daily', methods=['GET'])
@swag_from({
    'summary': 'Obtenir les offres d\'emploi quotidiennes',
    'description': 'Récupère et enregistre les offres d\'emploi quotidiennes.',
    'responses': {
        200: {'description': 'Liste des offres d\'emploi'},
        404: {'description': 'Aucune offre trouvée pour aujourd\'hui.'},
        500: {'description': 'Erreur interne du serveur'}
    }
})
def get_daily_postings_route():
    try:
        daily_postings = get_daily_postings()
        if daily_postings:
            save_job_postings(daily_postings)  # Enregistre dans la table job_postings
            return jsonify(daily_postings), 200
        else:
            return jsonify({"message": "No postings fetched for today."}), 404
    except Exception as e:
        logger.error(f"Error in /job-postings/daily: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/job-postings/historical', methods=['GET'])
@swag_from({
    'summary': 'Obtenir les offres historiques',
    'description': 'Récupère et enregistre les offres historiques dans une période spécifique.',
    'parameters': [
        {'name': 'start_date', 'in': 'query', 'type': 'string', 'required': True, 'description': 'Date de début (YYYY-MM-DD)'},
        {'name': 'end_date', 'in': 'query', 'type': 'string', 'required': True, 'description': 'Date de fin (YYYY-MM-DD)'}
    ],
    'responses': {
        200: {'description': 'Liste des offres historiques'},
        400: {'description': 'Format de date invalide'},
        500: {'description': 'Erreur interne du serveur'}
    }
})
def get_historical_postings_route():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    try:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        logger.debug(f"Parsed dates: start_date={start_date}, end_date={end_date}")
    except ValueError:
        logger.error("Invalid date format, should be YYYY-MM-DD")
        return jsonify({"error": "Invalid date format, please use YYYY-MM-DD."}), 400

    try:
        historical_postings, _ = fetch_historical_postings(start_date, end_date)
        if historical_postings:
            save_historical_job_postings(historical_postings)  # Enregistre dans la table historical_job_postings
            return jsonify(historical_postings), 200
        else:
            return jsonify({"message": "No historical postings fetched."}), 404
    except Exception as e:
        logger.error(f"Error in /job-postings/historical: {str(e)}")
        return jsonify({"error": "Error fetching historical postings."}), 500

@app.route('/stats/jobs-by-department', methods=['GET'])
@swag_from({
    'summary': 'Obtenir le nombre d\'offres par département',
    'description': 'Récupère le nombre d\'offres d\'emploi pour chaque département.',
    'responses': {
        200: {
            'description': 'Nombre d\'offres par département',
            'content': {'application/json': {'example': {'75': 120, '92': 50}}}
        }
    }
})
def jobs_by_department():
    department_counts = (
        db.session.query(HistoricalJobPosting.department, func.count(HistoricalJobPosting.id))
        .filter(HistoricalJobPosting.department.isnot(None))
        .group_by(HistoricalJobPosting.department)
        .all()
    )
    return jsonify({dep: count for dep, count in department_counts})

@app.route('/stats/contract-type-evolution', methods=['GET'])
@swag_from({
    'summary': 'Évolution des types de contrats',
    'description': 'Récupère le nombre d\'offres par type de contrat.',
    'responses': {
        200: {
            'description': 'Nombre d\'offres par type de contrat',
            'content': {'application/json': {'example': {'CDI': 80, 'CDD': 40}}}
        }
    }
})
def contract_type_evolution():
    contract_counts = (
        db.session.query(func.coalesce(HistoricalJobPosting.contract_type, 'Unknown'), func.count(HistoricalJobPosting.id))
        .group_by(HistoricalJobPosting.contract_type)
        .all()
    )
    return jsonify({ctype: count for ctype, count in contract_counts})

@app.route('/stats/jobs-by-commune', methods=['GET'])
@swag_from({
    'summary': 'Obtenir le nombre d\'offres par commune',
    'description': 'Récupère le nombre d\'offres d\'emploi pour chaque commune.',
    'responses': {
        200: {
            'description': 'Nombre d\'offres par commune',
            'content': {'application/json': {'example': {'Paris': 100, 'Lyon': 50}}}
        }
    }
})
def jobs_by_commune():
    commune_counts = (
        db.session.query(HistoricalJobPosting.commune, func.count(HistoricalJobPosting.id))
        .filter(HistoricalJobPosting.commune.isnot(None))
        .group_by(HistoricalJobPosting.commune)
        .all()
    )
    return jsonify({commune: count for commune, count in commune_counts})

# Initialiser la base de données si nécessaire
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
