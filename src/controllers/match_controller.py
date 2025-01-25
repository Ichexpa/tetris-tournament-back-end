from flask import request
from flask import current_app as app
from flask import jsonify
from flask import abort
from flask import Blueprint

from src.models.matches import Match
from src.repositories.match_repository import MatchRepository
from src.db import DbError
from mysql.connector.errors import IntegrityError

match_routes_bp = Blueprint("match_bp",__name__,url_prefix="/api/match")

@match_routes_bp.route("/<int:match_id>",methods=["GET"])
def get_matches_by_id():
    pass