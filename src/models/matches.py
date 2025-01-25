class Match:
    def __init__(self,**kwargs):
        self.id = kwargs.get("id")
        self.roudn = kwargs.get("round")
        self.player1_id = kwargs.get("player1_id")
        self.player2_id = kwargs.get("player2_id")
        self.score_p1 = kwargs.get("score_p1")
        self.score_p2 = kwargs.get("score_p2")
        self.winner_id = kwargs.get("winner_id")
        self.tournament_id = kwargs.get("tournament_id")
        self.next_match_id = kwargs.get("next_match_id")
    
    def __repr__(self):
        return f"<Match {id}"