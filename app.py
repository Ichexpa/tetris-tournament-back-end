from flask import Flask
from dotenv import load_dotenv
import os
from config import *
from src.db import Database
from src.controllers import *
from flask_cors import CORS
from src.utils.jwt_config import init_jwt
from src.utils.error_handlers import register_error_handlers
from src.controllers.tournament_controller import tournament_routes_bp
from src.controllers.auth_controller import auth_routes_bp
from src.controllers.player_controller import player_routes_bp
from src.controllers.organizer_controller import organizer_routes_bp
from src.controllers.match_controller import match_routes_bp
from src.controllers.tournament_player_controller import tournament_player_bp

load_dotenv()

def create_app():
    """Application factory function."""
    app = Flask(__name__)
    # Enable CORS for all domains
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Load the configuration
    env = os.getenv("FLASK_ENV", "development").lower()

    print(f"Running in {env} mode")

    class_config = {
        "production": ProductionConfig,
        "development": DevelopmentConfig,
        "testing": TestingConfig,
    }.get(env, DevelopmentConfig)

    app.config.from_object(class_config)

    # Inicializar JWT
    init_jwt(app)

    # Registrar manejadores de errores
    register_error_handlers(app)

    # Initialize the database pool

    app.db = Database(class_config)

    # Register 

    
    app.register_blueprint(auth_routes_bp)    
    app.register_blueprint(player_routes_bp)
    app.register_blueprint(organizer_routes_bp)
    app.register_blueprint(tournament_routes_bp)
    app.register_blueprint(tournament_player_bp) 
    app.register_blueprint(match_routes_bp)
    
    @app.route("/")
    def home():
        return "Welcome to Tetris API!"

    return app
