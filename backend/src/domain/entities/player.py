class Player:
    def __init__(self, player_id: int, name: str, position: str, per: float):
        self.player_id = player_id
        self.name = name
        self.position = position
        self.per = per

    def __repr__(self):
        return f"Player(id={self.player_id}, name='{self.name}', position='{self.position}', per={self.per})"