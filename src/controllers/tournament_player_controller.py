from flask import request
from flask import current_app as app
from flask import jsonify
from flask import abort
from flask import Blueprint

from src.models.tournament_players import TournamentPlayers
from src.repositories.tournament_players_repository import TournamentPlayersRepository
from src.db import DbError
from mysql.connector.errors import IntegrityError
from exceptions.exceptions_database import UniqueViolationError

tournament_player_bp = Blueprint("tournament_player_bp",__name__,url_prefix="/api/players-tournament")

@tournament_player_bp.route("/sign",methods=["POST"])
def sing_tournament():
    register_data = TournamentPlayers(player_id= request.json.get("player_id"),
                                                   tournament_id = request.json.get("tournament_id"))
    try:
        result = TournamentPlayersRepository(app.db).register_tournament(register_data)
    except IntegrityError:
       abort(404)
    except UniqueViolationError:
        return jsonify({"message":"Jugador ya registrado en el torneo"}),400
    else:
        if result:
           return jsonify({"message":"Registrado exitosamente al torneo"}),202
        return jsonify({"message":"No se ha podido registrar al torneo"}),400
