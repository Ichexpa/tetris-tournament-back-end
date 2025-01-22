class TournamentPlayers():

    def __init__(self,**kwargs):
        self.id  = kwargs.get("id")
        self.player_id = kwargs.get("player_id")
        self.tournament_id = kwargs.get("tournament_id")
        self.registered_date = kwargs.get("registered_date")
        self.confirm_date = kwargs.get("confirm_register_date")
    
    def __repr__(self):
        return f'<TournamentPlayersRegister> {self.id}'