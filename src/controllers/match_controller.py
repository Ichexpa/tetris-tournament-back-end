from flask import request
from flask import current_app as app
from flask import jsonify
from flask import abort
from flask import Blueprint

from src.models.match import Match
from src.repositories.match_repository import MatchRepository
from src.db import DbError
from mysql.connector.errors import IntegrityError

match_routes_bp = Blueprint("match_bp",__name__,url_prefix="/api/match")

@match_routes_bp.route("/<int:match_id>",methods=["GET"])
def get_matches_by_id(match_id):
    try:
        match = MatchRepository(app.db).get_match_by_id(Match(id=match_id))
    except DbError:
        abort(500)
    else:
        return jsonify({
                    "id" : match.id,
                    "round" : match.round,
                    "player1_id" : match.player2_id,
                    "player2_id" : match.player2_id,
                    "score_p1" : match.score_p1,
                    "score_p2" : match.score_p2,
                    "winner_id" : match.winner_id,
                    "tournament_id" : match.tournament_id,
                    "next_match_id" : match.next_match_id
        })
    

@match_routes_bp.route("/update_score",methods=["PATCH"])
def update_score():
    data_match = Match(**request.json)
    try:
        MatchRepository(app.db).update_brackets_results(data_match)
    except IntegrityError:
        abort(404)
    else:
        return jsonify({"message":"Se actualizaron los resultados con éxito"}),201 

