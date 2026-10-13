class Player:
    def __init__(self) -> None:
        self.clues = []

    def add_clue(self, clue_id: str) -> None:
        if clue_id not in self.clues:
            self.clues.append(clue_id)

    def has_clue(self, clue_id: str) -> bool:
        return clue_id in self.clues
