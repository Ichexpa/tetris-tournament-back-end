from src.models.tournament import Tournament
from src.models.user import Player
from mysql.connector.errors import IntegrityError,DatabaseError
from src.exceptions.exceptions_database import NotValidCapacity,FutureDateNotAllowedError,StatusNotAllowed,InsufficentsPlayers
from datetime import datetime
from src.utils.repository_functions import mix_id_players
from flask import current_app as app
from src.repositories.tournament_players_repository import TournamentPlayersRepository
from src.utils.validate_functions import valid_date
class TournamentRepository():

    def __init__(self,db):
        self.db = db
    

    def start_tournament(self,tournament:Tournament):
        """Crea un torneo a partir de dos procedimientos, pero antes verifica que el torneo
         tenga los jugadores necesarios para inciar, luego mezcla sus ids para pasarlos al procedimiento """
        tournament  = self.get_tournament_by_id(tournament)
        list_participants  = TournamentPlayersRepository(app.db).get_participants_tournament(tournament)
        if(tournament.capacity == len(list_participants)):
            mixed_ids = mix_id_players(list_participants)
            with self.db.get_connection() as conn:
                try:
                    cursor = conn.cursor()
                    cursor.callproc("generate_initial_matches",(tournament.id,mixed_ids))
                    cursor.callproc("link_tournament_matches",(tournament.id,))
                except IntegrityError:
                    conn.rollback()
                    raise
                else:
                    conn.commit()
                    self.update(Tournament(id=tournament.id,status="En curso"))
                    
        else:
            print("Faltan jugadores")
            raise InsufficentsPlayers
        


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
        valid_capacity = [8,16,32,64]
        capacity = int(tournament.capacity)
        if(capacity not in valid_capacity):
            raise NotValidCapacity
        if(not valid_date(tournament.start_date,tournament.end_date)):
            raise FutureDateNotAllowedError
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
                                 tournament.best_of or 3,
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
                except DatabaseError as e:
                    conn.rollback()
                    if e.errno == 1265:
                        raise StatusNotAllowed              
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
   
    def get_tournament_by_id(self,tournament:Tournament):
        if not tournament.id:
            raise KeyError
        try:
            query = "SELECT * FROM tournaments WHERE id=%s"
            with self.db.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query,(tournament.id,))
                result = cursor.fetchone()
                if result:
                    return Tournament(id=result["id"],
                                      name=result["name"],
                                      capacity=result["capacity"],
                                      total_points=result["total_points"],
                                      organizer_id=result["organizer_id"],
                                      status=result["status"],
                                      start_date=result["start_date"],
                                      end_date=result["end_date"],
                                      best_of = result["best_of"] )
                else:
                    return None
        except IntegrityError:
            raise  

    def get_players_inscribed_tournament(self,tournament:Tournament):
        """Devuelve todos los players inscritos en un torneo especifico"""
        if not tournament.id:
            raise KeyError
        try:
            query = """SELECT  p.id as player_id, u.first_name,u.last_name,u.email,p.score 
            FROM tournamentsxplayers tp INNER JOIN
            players p ON p.id = tp.player_id INNER JOIN 
            users u ON u.id = p.user_id WHERE tp.tournament_id=%s"""
            with self.db.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query,(tournament.id,))
                results = cursor.fetchall()
                players_list = []
                for result in results:
                        players_list.append(Player(id=result["player_id"],
                                    first_name=result["first_name"],
                                    last_name=result["last_name"],
                                    email=result["email"],
                                    score=result["score"] ))
                return players_list
        except IntegrityError:
            raise   
    
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
        
    def get_history_tournament_player(self,player:Player):
        if not player.id:
            raise KeyError
        try:
            query= """SELECT t.id AS tournament_id,t.name AS tournament_name,t.capacity,t.total_points,
                t.status,t.start_date,t.end_date,t.best_of,pr.player_id,MAX(pr.round) AS max_round
            FROM (SELECT tournament_id, player1_id AS player_id, round FROM matches UNION ALL
                SELECT tournament_id, player2_id AS player_id, round FROM matches
            ) AS pr INNER JOIN tournaments t ON pr.tournament_id = t.id WHERE pr.player_id = %s
                GROUP BY t.id, t.name, t.capacity, t.total_points, t.organizer_id, t.status, 
                t.start_date, t.end_date, t.best_of, pr.player_id ORDER BY t.start_date DESC;"""
            with self.db.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query,(player.id,))
                results = cursor.fetchall()                
                matches_list = []
                for result in results :
                     matches_list.append(result)
        except IntegrityError:
            raise
        else:
            return matches_list           