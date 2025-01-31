from flask import request
from flask import current_app as app
from flask import jsonify
from flask import abort
from flask import Blueprint

from src.models.tournament import Tournament
from src.models.user import Player
from src.repositories.tournament_repository import TournamentRepository
from src.db import DbError
from mysql.connector.errors import IntegrityError
from src.exceptions.exceptions_database import InsufficentsPlayers

tournament_routes_bp = Blueprint("tournament_bp",__name__,url_prefix="/api/tournament")

@tournament_routes_bp.route("/",methods=["GET"])
def get_tournaments():
    tournaments = TournamentRepository(app.db)
    filter = request.args
    if tournaments:
        return jsonify(tournaments.find_all(filter)),200
    else:
        abort(404)

@tournament_routes_bp.route("/create",methods=["POST"])
def create_tournament():
    tournament_to_create = Tournament(name=request.json.get("name"),
                                      capacity=request.json.get("capacity"),
                                      total_points=request.json.get("total_points"),
                                      organizer_id=request.json.get("organizer_id"),
                                      status=request.json.get("status"),
                                      start_date=request.json.get("start_date"),
                                      end_date=request.json.get("end_date"),
                                      best_of=request.json.get("best_of"))
    try:
        tournament = TournamentRepository(app.db).save(tournament_to_create)
    except IntegrityError:
        abort(404)
    else:
        if tournament.id:
            return jsonify(tournament.__dict__),200
        else:
            abort(505)

@tournament_routes_bp.route("/update",methods=["PATCH"])
def update_tournament():    
    data_t = Tournament(**request.json)
    try:
        TournamentRepository(app.db).update(data_t)
    except KeyError:
        return jsonify({"message":"No se envio un id para la actualizacion"}),400 
    except IntegrityError:
        abort(404)
    else:
        return jsonify({"message":"Se actualizo el torneo con éxito"}),201 

@tournament_routes_bp.route("/<int:tournament_id>",methods=["DELETE"])
def delete_tournament(tournament_id):    
    try:
        tournament = Tournament(id=tournament_id)
        print(tournament.id)
        TournamentRepository(app.db).delete(tournament)
    except IndexError:
        return jsonify({"message":"No se envio un id para la eliminacion"}),204
    except IntegrityError:
        abort(404)
    else:
        return jsonify({"message":"Se elimino el torneo con éxito"}),204
    
@tournament_routes_bp.route("/brackets/<int:tournament_id>")
def get_all_matches_tournament(tournament_id):
    try:
        tournament = Tournament(id=tournament_id)
        list_matches  = TournamentRepository(app.db).get_all_matches_tournament(tournament)
    except KeyError:
        return jsonify({"message":"No se envio el id del torneo"}),204
    except IntegrityError:
        abort(404)
    else:
        return jsonify(list_matches),200

@tournament_routes_bp.route("/start_tournament",methods = ["POST"])
def start_tournament():
    try:        
        tournament = Tournament(**request.json)
        TournamentRepository(app.db).start_tournament(tournament)
    except InsufficentsPlayers:
        return jsonify({"message":"Faltan jugadores para iniciar el torneo"}),400
    except IntegrityError:
        abort(404)
    else:
        return jsonify({"message":"Torneo inciado con exito"}),200
    
@tournament_routes_bp.route("/player_inscribed/<int:tournament_id>",methods = ["GET"])
def players_inscribed_tournament(tournament_id):
    try:        
        tournament = Tournament(id=tournament_id)
        list_players = TournamentRepository(app.db).get_players_inscribed_tournament(tournament)
    except IntegrityError:
        abort(404)
    else:
        lista_player_dict = [obj.__dict__ for obj in list_players]
        return jsonify(lista_player_dict),200
    
@tournament_routes_bp.route("/player_history/<int:player_id>",methods = ["GET"])
def players_history_matches(player_id):
    try:        
        player = Player(id=player_id)
        list_matches = TournamentRepository(app.db).get_history_tournament_player(player)
    except IntegrityError:
        abort(404)
    else:
        return jsonify(list_matches),200
    
@tournament_routes_bp.route("/<int:tournament_id>",methods = ["GET"])
def get_tournament_by_id(tournament_id):
    try:        
        tournament = Tournament(id=tournament_id)
        result = TournamentRepository(app.db).get_tournament_by_id(tournament)
    except IntegrityError:
        abort(404)
    else:
        return jsonify(result.__dict__),200

@tournament_routes_bp.route("/player_ranking",methods = ["GET"])
def players_ranking():
    try:
        ranking_list = TournamentRepository(app.db).get_ranking_player()
        if ranking_list is None: 
            return jsonify({"error": "No se pudo obtener el ranking"}), 500
        return jsonify(ranking_list), 200
    except IntegrityError:
        abort(404)
