from flask import request
from flask import current_app as app
from flask import jsonify
from flask import abort
from flask import Blueprint

from src.models.user import User, Player
from src.services.auth_service import AuthService, AuthPasswordError
from src.db import DbError
from flask_jwt_extended import jwt_required, get_jwt

auth_routes_bp = Blueprint('auth_bp', __name__, url_prefix="/api/auth")

@auth_routes_bp.route("/register", methods=["POST"])
def register_player():
    player_to_register = Player(
                            email=request.form.get("email", ''),
                            password=request.form.get("password", ''),
                            first_name=request.form.get("first_name", ''),
                            last_name=request.form.get("last_name", ''),
                            score=request.form.get("score", None),
                            ranking=request.form.get("ranking", None),
    )
    try:
        saved_player = AuthService(app.db).create_player(player_to_register)
    except DbError:
        abort(500)
    except AuthPasswordError:
        return jsonify({"message": "Non conforming password"}), 401
    except ValueError:
        return jsonify({"message": "Empty email"}), 401
    else:
        if saved_player.id:
            return jsonify({"message": f"Player {saved_player.email} successfully saved"}), 200
        else:
            return jsonify({"message": "Integrity error: email duplicated."}), 500

@auth_routes_bp.route('/login', methods=['POST'])
def login():
    user = User(email=request.form.get("email", ''),
                password=request.form.get("password", ''))
    print("EMAIL " + request.form.get("email", ''))
    print("CONTRASEÑA " + request.form.get("password", ''))
    token, result = AuthService(app.db).login(user)
    if token:
        return jsonify({"token": token, "role": result}), 200
        
    if result == "INVALID_CREDENTIALS":
        return jsonify({
            "error": "Credenciales inválidas",
            "mensaje": "Credenciales inválidas. Por favor, revisa tu email y contraseña."
        }), 401
    else:
        abort(500)

@auth_routes_bp.route("/validate", methods=["GET"])
@jwt_required()
def validate_token():
    """Valida el token JWT y retorna la información del usuario"""
    try:
        claims = get_jwt()
        user_id = claims.get("user_id")
        role = claims.get("role")
        
        if role == "player":
            user = AuthService(app.db).get_player(user_id)
        else:
            user = AuthService(app.db).get_organizer(user_id)
        
        if user:
            return jsonify({
                "id": user.user_id,
                "name": f"{user.first_name} {user.last_name}",
                "email": user.email,
                "role": role,
                "score": user.score if role == "player" else None,
                "ranking": user.ranking if role == "player" else None,
            }), 200
        else:
            abort(404)
            
    except Exception as e:
        app.logger.error(f"Error validando token: {str(e)}")
        abort(500)
