import os
from flask import Flask
#from app.config import MAIL_PASSWORD, MAIL_PORT, MAIL_SERVER, MAIL_USERNAME, MAIL_USE_TLS, MAIL_USE_SSL
from app.utils import *
from flask_mailman import Mail
# Importation des blueprints de l'application
# Chaque blueprint contient des routes pour l'application
from app.views.home import home_bp
from app.views.auth import auth_bp
from app.views.user import user_bp
from app.views.pet import pet_bp
# Fonction automatiquement appelée par le framework Flask lors de l'exécution de la commande python -m flask run permettant de lancer le projet
# La fonction retourne une instance de l'application créée

mail = Mail()

def create_app():

    

    # Crée l'application Flask
    app = Flask(__name__)
    
    app.config['MAIL_SERVER'] = os.environ.get(MAIL_SERVER)
    app.config['MAIL_PORT'] = os.environ.get(MAIL_PORT)
    app.config['MAIL_USERNAME'] = os.environ.get(MAIL_USERNAME)
    app.config['MAIL_PASSWORD'] = os.environ.get(MAIL_PASSWORD)
    app.config['MAIL_USE_TLS'] = os.environ.get(MAIL_USE_TLS)
    app.config['MAIL_USE_SSL'] = os.environ.get(MAIL_USE_SSL)
    
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), "config.py"))
    # Enreigstrement des blueprints de l'application.
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(pet_bp)

    # On retourne l'instance de l'application Flask
    return app
