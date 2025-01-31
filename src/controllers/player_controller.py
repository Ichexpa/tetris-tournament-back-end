from flask import request
from flask import current_app as app
from flask import jsonify
from flask import abort
from flask import Blueprint

from src.models.user import Player
from src.services.auth_service import AuthService
from src.repositories.user_repository import UserRepository
from src.db import DbError

player_routes_bp = Blueprint(
    "player_bp", __name__, url_prefix="/api/users/players"
)


@player_routes_bp.route("/<int:user_id>", methods=["GET"])
def get_players(user_id):
    try:
        player = AuthService(app.db).get_player(user_id)
    except DbError:
        abort(500)
    else:
        if player and isinstance(player, Player):
            return (
                jsonify(
                    {
                        "id": player.id,
                        "email": player.email,
                        "first_name": player.first_name,
                        "last_name": player.last_name,
                        "user_id": player.user_id,
                        "score": player.score,
                        "created_at": player.created_at,
                    }
                ),
                200,
            )
        abort(404)

@player_routes_bp.route("/by_id/<int:player_id>", methods=["GET"])
def get_players_by_id(player_id):
    try:
        player = UserRepository(app.db).get_player_by_id(player_id)
    except DbError:
        abort(500)
    else:
        return jsonify(player),200
