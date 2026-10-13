from collections.abc import Callable


class Interactable:
    def __init__(
        self,
        interactable_id: str,
        name: str,
        location_id: str,
        description: str | Callable[[], str],
        clue_id: str | None = None,
    ) -> None:
        self.interactable_id = interactable_id
        self.name = name
        self.location_id = location_id
        self.description = description
        self.clue_id = clue_id

    def get_description(self) -> str:
        if callable(self.description):
            return self.description()
        return self.description
