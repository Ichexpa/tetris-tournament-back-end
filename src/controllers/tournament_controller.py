from flask import request
from flask import current_app as app
from flask import jsonify
from flask import abort
from flask import Blueprint

from src.models.tournament import Tournament
from src.repositories.tournament_repository import TournamentRepository
from src.db import DbError
from mysql.connector.errors import IntegrityError

tournamnet_routes_bp = Blueprint("tournament_bp",__name__,url_prefix="/api/tournament")

@tournamnet_routes_bp.route("/",methods=["GET"])
def get_tournaments():
    tournaments = TournamentRepository(app.db)
    filter = request.args
    print(filter)
    if tournaments:
        return jsonify(tournaments.find_all(filter)),200
    else:
        abort(404)

@tournamnet_routes_bp.route("/create",methods=["POST"])
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

@tournamnet_routes_bp.route("/update",methods=["PATCH"])
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

@tournamnet_routes_bp.route("/<int:tournament_id>",methods=["DELETE"])
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