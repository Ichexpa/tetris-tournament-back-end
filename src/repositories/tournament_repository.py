from src.models.tournament import Tournament
from mysql.connector.errors import IntegrityError

class TournamentRepository():

    def __init__(self,db):
        self.db = db
    
    def find_all(self) -> list[dict]:
        """Muestra todos los torneos creados"""

        with self.db.get_connection() as conn:
            cursor = conn.cursor(dictionary = True)
            cursor.execute("SELECT * FROM tournaments")
            result = cursor.fetchall()
            return result
    
    def save(self,tournament:Tournament):
        """Crea un torneo"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                res = cursor.callproc("create_tournament",
                                (tournament.name,
                                 tournament.capacity,
                                 tournament.total_points,
                                 tournament.organizer_id,
                                 tournament.status or "Activo",
                                 tournament.start_date,
                                 tournament.end_date,
                                 None))
            except IntegrityError:
                conn.rollback()
                raise
            else:
                conn.commit()
                tournament.id = res[-1]
                return tournament

