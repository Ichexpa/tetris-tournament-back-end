from src.models.user import Player, Organizer
from typing import Union
from mysql.connector.errors import IntegrityError


class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Union[Player, Organizer]:
        """Obtiene un usuario por su id, ya sea estudiante u organizador."""

        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                query = """
                SELECT u.id AS user_id, u.email, p.id AS player_id, o.id AS organizer_id,
                u.email, u.first_name, u.last_name, u.created_at,
                p.score,
                CASE WHEN p.id IS NOT NULL THEN TRUE ELSE FALSE END AS is_player
                FROM users u
                LEFT JOIN players p ON u.id = p.user_id
                LEFT JOIN organizers o ON u.id = o.user_id
                WHERE u.id = %s
                """
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()
                if result:
                    if result["is_player"]:
                        user = Player(
                            id=result["player_id"],
                            user_id=result["user_id"],
                            first_name=result["first_name"],
                            last_name=result["last_name"],
                            score=result["score"]
                        )
                    else:
                        user = Organizer(
                            id=result["organizer_id"],
                            user_id=result["user_id"],
                            first_name=result["first_name"],
                            last_name=result["last_name"],
                            created_at=result["created_at"],
                        )
                    user.email = result["email"]
                    return user
                return None
        except:
            raise

    def get_user_by_email(self, email: str) -> Union[Player, Organizer]:
        """Obtiene un usuario por su email, ya sea jugador u organizador."""

        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                query = """
                SELECT u.id AS user_id, u.password, p.id AS player_id, o.id AS organizer_id,
                CASE WHEN p.id IS NOT NULL THEN TRUE ELSE FALSE END AS is_player
                FROM users u
                LEFT JOIN players p ON u.id = p.user_id
                LEFT JOIN organizers o ON u.id = o.user_id
                WHERE u.email = %s
                """
                cursor.execute(query, (email,))
                result = cursor.fetchone()
                print(result)
                if result:
                    if result["is_player"]:
                        user = Player(
                            id=result["player_id"],
                            user_id=result["user_id"],
                            password=result["password"],
                        )
                    else:
                        user = Organizer(
                            id=result["organizer_id"],
                            user_id=result["user_id"],
                            password=result["password"],
                        )   
                    user.email = email
                    
                    return user
                   
                return None
        except:
            raise

    def get_players(self, filter_criteria: dict = None) -> list:
        """Devuelve una lista de jugadores.
        Args:
            filter_criteria (dict): Criterios de filtrado.
        Returns:
            list: Lista de jugadores.
        """
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                query = """
                SELECT p.*, u.email, u.first_name, u.last_name, u.created_at
                FROM players p
                JOIN users u ON p.user_id = u.id
                """
                if filter_criteria:
                    query += " WHERE "
                    query += " AND ".join(
                        f"{key} = %s" for key in filter_criteria.keys()
                    )
                    cursor.execute(query, tuple(filter_criteria.values()))
                else:
                    cursor.execute(query)
                results = cursor.fetchall()
                players = []
                for result in results:
                    player = Player(
                        id=result["id"],
                        email=result["email"],
                        first_name=result["first_name"],
                        last_name=result["last_name"],                        
                        score=result["score"],
                        created_at=result["created_at"]
                    )
                    players.append(player)
                return player
        except:
            raise

    def get_organizers(self, filter_criteria: dict = None) -> list:
        """Devuelve una lista de organizadores.
        Args:
            filter_criteria (dict, optional): Criterios de filtrado. Por defecto es None.
        Returns:
            list: Lista de organizadores.
        """
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                query = """
                SELECT p.*, u.email, u.first_name, u.last_name, u.created_at
                FROM organizers o
                JOIN users u ON o.user_id = u.id
                """
                if filter_criteria:
                    query += " WHERE "
                    query += " AND ".join(
                        f"{key} = %s" for key in filter_criteria.keys()
                    )
                    cursor.execute(query, tuple(filter_criteria.values()))
                else:
                    cursor.execute(query)
                results = cursor.fetchall()
                organizers = []
                for result in results:
                    organizer = Organizer(
                        id=result["id"],
                        email=result["email"],
                        first_name=result["first_name"],
                        last_name=result["last_name"],
                        created_at=result["created_at"]
                    )
                    organizers.append(organizer)
                return organizers
        except:
            raise

    def create_player(self, player: Player) -> Player:
        """Llama al procedimiento almacenado para crear un jugador."""
        with self.db.get_connection() as conn:
            try:
                cursor = conn.cursor()
                res = cursor.callproc(
                    "create_player",
                    (
                        player.email,
                        player.password,
                        player.first_name,
                        player.last_name,
                        None,
                    ),
                )
            except IntegrityError:
                conn.rollback()
                raise
            else:
                conn.commit()
                player.id = res[-1]
                player.password = None
                return player
