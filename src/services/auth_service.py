import json

import bcrypt
from flask import jsonify
from flask_jwt_extended import create_access_token

from src.models.user import User, Player, Organizer
from src.repositories.user_repository import UserRepository
from mysql.connector.errors import IntegrityError
from src.db import DbError

class AuthPasswordError(Exception):
    pass


class AuthService:
    def __init__(self, db):
        try:
            self.user_repository = UserRepository(db)
        except DbError:
            raise

    def login(self, user: User) -> tuple:
        try:
            # Intentar obtener el usuario por su email
            
            saved_user = self.user_repository.get_user_by_email(user.email)

            print(saved_user)            
            if not saved_user:
                return None, "INVALID_CREDENTIALS"
                
            # Segunda validación: contraseña correcta    
            user_pass_bytes = user.password.encode("utf-8")
            ##print("Contraseña encodeada " + user_pass_bytes)
            if not bcrypt.checkpw(user_pass_bytes, saved_user.password):
                return None, "INVALID_CREDENTIALS"
            
            # Si las credenciales son correctas
            if isinstance(saved_user, Player):
                token = create_access_token(
                    json.dumps(
                        {"user_id": saved_user.user_id, "role": "player"}
                    )
                )
                return token, "player"
            elif isinstance(saved_user, Organizer):
                token = create_access_token(
                    json.dumps(
                        {"user_id": saved_user.user_id, "role": "organizer"}
                    )
                )
                return token, "organizer"
                
        except Exception as e:
            return None, "SERVER_ERROR"

    def create_player(self, player: Player):
        if not player.email:
            raise ValueError(f"Email empty.")
        if not (len(player.password) > 8 and len(player.password) < 16):
            raise AuthPasswordError(
                f"Non conforming password. Password length: {len(player.password)}"
            )
        try:
            player.password = bcrypt.hashpw(
                player.password.encode("utf-8"), bcrypt.gensalt()
            )
            saved_player = self.user_repository.create_player(player)
        except IntegrityError as err:
            # devolver el mismo player, sin id
            return player
        else:
            # devolver el player guardado con su id
            return saved_player

    def get_player(self, user_id: int) -> Player:
        player = self.user_repository.get_user_by_id(user_id)
        if isinstance(player, Player):
            return player
        else:
            return None

    def get_organizer(self, user_id: int) -> Organizer:
        organizer = self.user_repository.get_user_by_id(user_id)
        if isinstance(organizer, Organizer):
            return organizer
        else:
            return None