import random

def mix_id_players(tournament_list_player):
    list_players = []
    for player in tournament_list_player:
        list_players.append(player.player_id)
    random.shuffle(list_players)    
    mixed_ids = mixed_ids = ','.join(str(player) for player in list_players)
    return mixed_ids

