class Event:
    def __init__(self, event_id: str, description: str, location_id: str) -> None:
        self.event_id = event_id
        self.description = description
        self.triggered = False
        self.location_id = location_id
        