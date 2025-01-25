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
   
    def get_all_matches_tournament(self,tournament:Tournament):
        if not tournament.id:
            raise KeyError
        try:
            query = """SELECT 
                        m.id AS match_id,
                        m.next_match_id,
                        m.round AS round,
                        m.score_p1,m.score_p2,
                        m.winner_id,p1.id AS player1_id,
                        CONCAT(u1.first_name," ",u1.last_name) AS player1_name,
                        p2.id AS player2_id,
                        CONCAT(u2.first_name," ",u2.last_name) AS player2_name
                        FROM matches m
                        LEFT JOIN players p1 ON m.player1_id = p1.id
                        LEFT JOIN users u1 ON u1.id = p1.user_id
                        LEFT JOIN players p2 ON m.player2_id = p2.id
                        LEFT JOIN users u2 ON u2.id = p2.user_id
                        WHERE m.tournament_id = %s
                        ORDER BY m.round, m.id;"""
            with self.db.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query,(tournament.id,))
                results = cursor.fetchall()                
                matches_list = []
                for result in results : 
                    matches_list.append({
                        "id": result["match_id"],
                        "nextMatchId": result["next_match_id"],
                        "tournamentRoundText": result["round"],
                        "participants": [
                            {
                                "id" : result["player1_id"],
                                "resultText" : result["score_p1"],
                                "isWinner" : (
                                result.get("player1_id") is not None and
                                result.get("player1_id") == result.get("winner_id")
                            ),
                                "name": result["player1_name"]
                            },
                            {
                                "id" : result["player2_id"],
                                "resultText" : result["score_p2"],
                                "isWinner": (
                                    result.get("player2_id") is not None and
                                    result.get("player2_id") == result.get("winner_id")
                                ),
                                "name": result["player2_name"]
                            }
                        ]
                    })                    
        except IntegrityError:
            raise
        else:
            return matches_list