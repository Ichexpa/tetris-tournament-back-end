from src.models.tournament import Tournament
from mysql.connector.errors import IntegrityError

class TournamentRepository():

    def __init__(self,db):
        self.db = db
    
    def find_all(self,filter:dict) -> list[dict]:
        """Devuelve todos los torneos. O devuelve los torneos en los que
        un jugador se inscribió.
        Filtros:
        user_id : Id del usuario  
        inscribed : false o true"""
        
        query = "SELECT * FROM tournaments"
        print(filter)
        with self.db.get_connection() as conn:
            cursor = conn.cursor(dictionary = True)
            if filter:            
                user_id =  filter.get("user_id")
                inscribed = filter.get("inscribed",False).lower() == 'true'
                query = """SELECT t.* FROM tournaments t 
                    LEFT JOIN tournamentsxplayers tp on tp.tournament_id=t.id AND tp.player_id = %s
                    WHERE tp.tournament_id"""
                if(user_id and inscribed):
                    query += " IS NOT NULL"
                if(user_id and not inscribed):
                    query += " IS NULL"
                cursor.execute(query,(user_id,))
                print(query) 
            else:        
                cursor.execute(query)
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
                                 tournament.best_of,
                                 None))
            except IntegrityError:
                conn.rollback()
                raise
            else:
                conn.commit()
                tournament.id = res[-1]
                return tournament

