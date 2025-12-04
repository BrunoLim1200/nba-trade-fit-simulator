from typing import List

class Team:
    def __init__(self, id: int, name: str, players: List[str]):
        self.id = id
        self.name = name
        self.players = players

    def add_player(self, player_name: str):
        self.players.append(player_name)

    def remove_player(self, player_name: str):
        self.players.remove(player_name)

    def get_players(self) -> List[str]:
        return self.players

    def __repr__(self):
        return f"Team(id={self.id}, name='{self.name}', players={self.players})"