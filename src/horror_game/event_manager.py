from .event import Event


class EventManager:
    def __init__(self) -> None:
        self.events = {}

    def add_event(self, event: Event) -> None:
        if event.event_id not in self.events:
            self.events[event.event_id] = event
        else:
            raise ValueError("Event already exists")

    def get_event(self, event_id: str) -> Event | None:
        return self.events.get(event_id)

    def get_events_by_location(self, location_id: str) -> list[Event]:
        return [event for event in self.events.values() if event.location_id == location_id]
    
