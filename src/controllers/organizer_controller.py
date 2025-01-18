from flask import current_app as app
from flask import jsonify
from flask import abort
from flask import Blueprint

from src.models.user import Organizer
from src.services.auth_service import AuthService
from src.db import DbError

organizer_routes_bp = Blueprint(
    "organizer_bp", __name__, url_prefix="/api/users/organizer"
)


@organizer_routes_bp.route("/<int:user_id>", methods=["GET"])
def get_organizer(user_id):
    try:
        organizer = AuthService(app.db).get_organizer(user_id)
    except DbError:
        abort(500)
    else:
        if organizer and isinstance(organizer, Organizer):
            return (
                jsonify(
                    {
                        "id": organizer.id,
                        "email": organizer.email,
                        "first_name": organizer.first_name,
                        "last_name": organizer.last_name,
                        "user_id": organizer.user_id,
                    }
                ),
                200,
            )
        abort(404)
