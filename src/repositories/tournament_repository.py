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

    def update(self,tournament:Tournament):
        """Actualiza un torneo de acuerdo a su id"""
        """Solo actualiza los campos enviados en la peticion"""

        try:            
            if(not tournament.id):
                raise KeyError
            tournament = tournament.__dict__
            id = tournament.pop("id")
            set_clause = ", ".join([f"{key} = %s" for key, value in tournament.items() if value is not None])
            values = [value for value in tournament.values() if value is not None]
            values.append(id)
            query = f"""UPDATE tournaments
                        SET {set_clause}
                        WHERE id = %s"""
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(query,tuple(values))
                except IntegrityError:
                    conn.rollback()
                    raise    
                else:
                    conn.commit()
        except KeyError:
            raise
    
    def delete(self, tournament: Tournament):
        """Eliminar un torneo de acuerdo a su id"""

        if not tournament.id:
            raise IndexError
        query = "DELETE FROM tournaments WHERE id = %s"
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (tournament.id,))
            except IntegrityError:
                conn.rollback()
                raise
            else:
                conn.commit()
   
    