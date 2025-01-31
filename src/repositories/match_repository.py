from src.models.match import Match
from flask import current_app as app
from mysql.connector.errors import IntegrityError
from src.repositories.tournament_repository import TournamentRepository
from src.models.tournament import Tournament
from mysql.connector.errors import IntegrityError


class MatchRepository():

    def __init__(self,db):
        self.db = db

    def update_brackets_results(self,match:Match):
        tornament = TournamentRepository(app.db).get_tournament_by_id(Tournament(id=match.tournament_id))
        tournament_format_score = 2 if tornament.best_of == 3 else 3
        set_clause = "score_p1=%s, score_p2=%s "
        if(tournament_format_score<=match.score_p1):
            set_clause+=f", winner_id = {match.player1_id}"
            if match.next_match_id is not None:                
                self.update_winner_next_match(Match(id=match.next_match_id,
                                                winner_id = match.player1_id))
            else:
                TournamentRepository(app.db).update(Tournament(id=tornament.id,status="Finalizado"))            
        
        elif (tournament_format_score<=match.score_p2):
            set_clause+=f", winner_id = {match.player2_id}"
            if match.next_match_id is not None:
                self.update_winner_next_match(Match(id=match.next_match_id,
                                                winner_id = match.player2_id))
            else:
                TournamentRepository(app.db).update(Tournament(id=tornament.id,status="Finalizado")) 
        query = f"""UPDATE matches
                        SET {set_clause}
                        WHERE id = %s"""
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query,(match.score_p1,match.score_p2,match.id))
            except IntegrityError:
                conn.rollback()
                raise             
            else:
                conn.commit()
         

    def get_match_by_id(self,match:Match):
        if not match.id:
            raise KeyError
        try:
            query = "SELECT * FROM matches WHERE id=%s"
            with self.db.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query,(match.id,))
                result = cursor.fetchone()                
                if result:
                    return Match(id = result["id"],
                                round = result["round"],
                                player1_id = result["player1_id"],
                                player2_id = result["player2_id"],
                                score_p1 = result["score_p1"],
                                score_p2 = result["score_p2"],
                                winner_id = result["winner_id"],
                                tournament_id = result["tournament_id"],
                                next_match_id = result["next_match_id"])
                else:
                    return None
        except IntegrityError:
            raise     

    def update_winner_next_match(self,match:Match):
        set_clause=None
        next_match = self.get_match_by_id(Match(id=match.id))
        if next_match:
            if not next_match.player1_id:
                set_clause = "player1_id = %s "
            else:
                set_clause = "player2_id = %s "

            query = f"""UPDATE matches
                            SET {set_clause}
                            WHERE id = %s"""        
            
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(query,(match.winner_id,match.id))
                except IntegrityError:
                    conn.rollback()
                    raise             
                else:
                    conn.commit()
        else:
            print("No se encontro el next match")

 