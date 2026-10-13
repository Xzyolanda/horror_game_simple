from .cleaning_status import RoomCleaningStatus
from .event import Event
from .event_manager import EventManager
from .game import Game, GameMap
from .interactable import Interactable
from .location import Location
from .player import Player
from .rule import Rule
from .rule_book import RuleBook


def main():
    # create map
    hotel = GameMap()
    reception = Location(
        "reception",
        "Reception",
        "No one is at the reception. A dim light flickers above the entrance.",
    )
    corridor = Location("corridor", "Corridor", "")
    room_409 = Location("room_409", "Room 409", "")
    staff_room = Location(
        "staff_room",
        "Staff Room",
        "A small break room with a kettle, a worn table, and lockers along one wall. "
        "Someone has left a mug to dry beside the sink.",
    )
    hotel.add_location(reception)
    hotel.add_location(corridor)
    hotel.add_location(room_409)
    hotel.add_location(staff_room)
    reception.add_connection(corridor.location_id)
    corridor.add_connection(reception.location_id)
    corridor.add_connection(room_409.location_id)
    corridor.add_connection(staff_room.location_id)
    room_409.add_connection(corridor.location_id)
    staff_room.add_connection(corridor.location_id)

    reception.add_interactable(
        Interactable(
            "guest_register",
            "Guest Register",
            "reception",
            "The register lists guests in Rooms 408 and 410, but there is no "
            "entry for Room 409. No pages are missing or visibly altered, and "
            "the room numbers appear consecutive.",
            clue_id="missing_room_409_entry",
        )
    )
    reception.add_interactable(
        Interactable(
            "telephone",
            "Telephone",
            "reception",
            "The telephone rests quietly on the desk. Its line is still live.",
        )
    )
    reception.add_interactable(
        Interactable(
            "handbook",
            "Handbook",
            "reception",
            "The night-shift handbook is on the desk. You need to pick it up "
            "before you can read its rules.",
        )
    )
    cleaning_status = RoomCleaningStatus()
    staff_room.add_interactable(
        Interactable(
            "cleaning_schedule",
            "Cleaning Schedule",
            "staff_room",
            cleaning_status.cleaning_schedule_description,
            clue_id="room_409_schedule",
        )
    )

    room_409.add_interactable(
        Interactable(
            "room_409_cleaning_record",
            "Cleaning Record",
            "room_409",
            cleaning_status.room_409_cleaning_record_description,
            clue_id="room_409_cleaning_record",
        )
    )
    hotel.validate_connections()

    # rules
    rule_001 = Rule(
        "rule_001",
        "All night-shift employees must remain inside the hotel until 6:00 AM.",
        True,
    )
    rule_002 = Rule(
        "rule_002", "Guests are not allowed to enter the hotel after 10:00 PM.", True
    )
    rule_003 = Rule("rule_003", "Room 409 has only one bed.", True)
    rule_book = RuleBook()
    rule_book.add_rule(rule_001)
    rule_book.add_rule(rule_002)
    rule_book.add_rule(rule_003)

    # Event 1 created.
    event_rulebook = Event(
        "reception_handbook",
        "A night-shift handbook is lying on the reception desk.",
        "reception",
    )
    event_room_409 = Event(
        "room_409_manager",
        "The door to Room 409 stands slightly open. Warm yellow light spills "
        "over an unmade bed and used towels on the floor.",
        "room_409",
    )
    event_manager = EventManager()
    event_manager.add_event(event_rulebook)
    event_manager.add_event(event_room_409)

    # initialize game with map and rulebook
    # and run it
    player = Player()
    game = Game(hotel, rule_book, event_manager, cleaning_status, player)
    game.run()


if __name__ == "__main__":
    main()
