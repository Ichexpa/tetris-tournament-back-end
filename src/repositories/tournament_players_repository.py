from src.models.tournament_players import TournamentPlayers
from mysql.connector.errors import IntegrityError
from src.exceptions.exceptions_database import UniqueViolationError
from src.models.tournament import Tournament

class TournamentPlayersRepository():

    def __init__(self,db):
        self.db = db
    
    def register_tournament(self,tournament_players : TournamentPlayers)->bool:
        """Registra a un competidor en un torneo"""
        if(self.is_exceeded(tournament_players.tournament_id) == 0):
            with self.db.get_connection() as conn:
                try:            
                    cursor = conn.cursor()
                    query = """INSERT INTO tournamentsxplayers(
                    player_id,tournament_id) VALUES((SELECT players.id 
                    FROM players 
                    INNER JOIN users ON players.user_id = users.id 
                    WHERE users.id = %s 
                    LIMIT 1),%s)"""          
                    cursor.execute(query,(tournament_players.player_id,
                                        tournament_players.tournament_id))
                    
                except IntegrityError as e:
                    conn.rollback()
                    if e.errno == 1062:
                        raise UniqueViolationError("Jugador ya registrado")
                    else :
                        raise e;
                else : 
                    conn.commit()
                    return True;
        else:
            return False
        
    def get_participants_tournament(self,tournament:Tournament):
        if not tournament.id:
            raise KeyError
        try:
            query="SELECT * FROM tournamentsxplayers WHERE tournament_id  = %s"
            with self.db.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query,(tournament.id,))
                list_participants = []
                results = cursor.fetchall()
                for result in results:
                    list_participants.append(TournamentPlayers(id=result["id"],
                                      player_id=result["player_id"],
                                      tournament_id=result["tournament_id"],))
                return list_participants
        except IntegrityError:
            raise 

    def is_exceeded(self,tournament_id):
        """Verfica si el torneo esta lleno"""

        with self.db.get_connection() as conn:
            try:
                cursor = conn.cursor()
                query = """SELECT 
                        EXISTS (
                            SELECT 1
                            FROM tournaments t
                            LEFT JOIN tournamentsxplayers tp 
                            ON %s = tp.tournament_id
                            GROUP BY t.id, t.capacity
                            HAVING COUNT(tp.id) > t.capacity
                        ) AS is_exceeded;"""
                cursor.execute(query, (tournament_id,))
                result = cursor.fetchone()    
            except IntegrityError:
                raise
            else:
                return result[0]
            
