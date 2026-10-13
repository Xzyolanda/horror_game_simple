from .interactable import Interactable


class Location:
    def __init__(self, location_id: str, name: str, description: str) -> None:
        self.location_id = location_id
        self.name = name
        self.description = description
        self.connections = []
        self.interactables: list[Interactable] = []

    def add_connection(self, location_id: str) -> None:
        if location_id not in self.connections:
            self.connections.append(location_id)

    def add_interactable(self, interactable: Interactable) -> None:
        if interactable.location_id != self.location_id:
            raise ValueError("Interactable belongs to a different location")
        if any(
            item.interactable_id == interactable.interactable_id
            for item in self.interactables
        ):
            raise ValueError("Interactable already exists")
        self.interactables.append(interactable)

    def get_interactables(self) -> list[Interactable]:
        return self.interactables.copy()

    def describe(self) -> None:
        print(f"You are at {self.name}.")
        print(self.description)

    def has_connection(self, location_id: str) -> bool:
        return location_id in self.connections

    def get_connections(self) -> list[str]:
        return self.connections.copy()

    def display_connections(self) -> None:
        connections = self.get_connections()
        if connections == []:
            print("This is a dead end.")
        else:
            print("You can go to the following locations:")
            for connection in connections:
                print(f"- {connection}")
