from .cleaning_status import RoomCleaningStatus
from .event_manager import EventManager
from .location import Location
from .player import Player
from .rule_book import RuleBook


class GameMap:
    def __init__(self):
        self.locations = {}

    def add_location(self, location: Location):
        if location.location_id not in self.locations:
            self.locations[location.location_id] = location
        else:
            raise ValueError("Location already exists")

    def get_location(self, location_id: str) -> Location | None:
        return self.locations.get(location_id)

    def validate_connections(self) -> None:
        for location in self.locations.values():
            for connection in location.connections:
                if connection not in self.locations:
                    raise ValueError(f"Connection {connection} does not exist")


class Game:
    def __init__(
        self,
        game_map: GameMap,
        rule_book: RuleBook,
        event_manager: EventManager,
        cleaning_status: RoomCleaningStatus,
        player: Player,
    ) -> None:
        self.game_map = game_map
        self.current_location_id = "reception"
        self.rule_book = rule_book
        self.event_manager = event_manager
        self.cleaning_status = cleaning_status
        self.player = player
        self.has_rule_book = False
        self.room_409_visits = 0
        self.room_409_locked = False
        self.hallucinating = False

    def move_to(self, location_id: str) -> bool:
        current_location = self.game_map.get_location(self.current_location_id)
        if (
            location_id in self.game_map.locations
            and current_location is not None
            and current_location.has_connection(location_id)
        ):
            leaving_room_409_after_second_visit = (
                self.current_location_id == "room_409"
                and self.room_409_visits >= 2
                and location_id != "room_409"
            )
            self.current_location_id = location_id

            if location_id == "room_409":
                self.room_409_visits += 1
            if leaving_room_409_after_second_visit:
                self.room_409_locked = True
                self.hallucinating = True
            return True
        return False

    def check_location_events(self) -> None:
        events = self.event_manager.get_events_by_location(self.current_location_id)
        for event in events:
            if event.triggered:
                continue
            print(event.description)
            if event.event_id == "reception_handbook":
                while True:
                    answer = (
                        input("Do you want to pick up the handbook? (yes/no): ")
                        .strip()
                        .lower()
                    )
                    if answer == "yes":
                        self.has_rule_book = True
                        print("You picked up the handbook.")
                        break
                    if answer == "no":
                        print("You decided not to pick up the handbook.")
                        break
                    print("Invalid input. Please answer 'yes' or 'no'.")
            elif event.event_id == "room_409_manager":
                self.handle_room_409_manager_event()
            event.triggered = True

    def handle_room_409_manager_event(self) -> None:
        print('"Oh, good. You\'re here."')
        print(
            "\"I'm the duty manager. Could you give me a hand with this room? "
            "Housekeeping didn't finish before their shift ended.\""
        )
        print(
            '"Just change the sheets and leave the towels by the bathroom door. '
            "I'll sort out the paperwork.\""
        )

        while True:
            choice = input(
                "How do you respond?\n1. Cooperate\n2. Question\n3. Refuse\n> "
            ).strip()

            if choice == "1":
                self.cleaning_status.mark_room_409_completed()
                print("You agree to help with the room.")
                print(
                    "Later, the cleaning record already bears your signature, "
                    "though you do not remember signing it."
                )
                return

            if choice == "2":
                self.cleaning_status.mark_room_409_completed()
                print(
                    "You ask why Room 409 needs cleaning if it is permanently "
                    "unoccupied."
                )
                print('"It is. It\'s always on the schedule."')
                print('"Please get the room ready."')
                return

            if choice == "3":
                self.cleaning_status.mark_room_409_completed()
                print("You cite the handbook and decline the request.")
                print('"All right. I\'ll ask the morning team to do it."')
                return

            print("Invalid choice. Please enter 1, 2, or 3.")

    def interact(self) -> None:
        current_location = self.game_map.get_location(self.current_location_id)
        if current_location is None:
            return

        interactables = current_location.get_interactables()
        if not interactables:
            print("There is nothing to inspect here.")
            return

        while True:
            print("What would you like to inspect?")
            for index, interactable in enumerate(interactables, start=1):
                print(f"{index}. {interactable.name}")
            print("0. Go back")

            choice = input("> ").strip()
            if choice == "0":
                return
            if not choice.isdigit():
                print("Invalid choice. Please enter a number from the menu.")
                continue

            index = int(choice)
            if not 1 <= index <= len(interactables):
                print("Invalid choice. Please select an item from the menu.")
                continue

            interactable = interactables[index - 1]
            print(interactable.get_description())
            self.record_clue(interactable)

    def record_clue(self, interactable) -> None:
        if interactable.clue_id is not None and not self.player.has_clue(
            interactable.clue_id
        ):
            self.player.add_clue(interactable.clue_id)

    def trigger_handover_ending(self) -> None:
        print(
            "Dawn light reaches the reception desk. It is time to complete the handover."
        )
        if len(self.player.clues) >= 3:
            print(
                "You write down the missing entry, the blank schedule, and the signed record."
            )
            print('Your supervisor replies: "The hotel has no Room 409."')
        else:
            print("You sign the handover without adding anything else.")
            print(
                "Outside, you check your employment file. It lists you as having "
                "worked at the hotel for many years."
            )

    def describe_room_409(self) -> None:
        print("You are at Room 409.")
        if self.room_409_visits == 1:
            print(
                "It looks like an ordinary hotel room: a single bed, a bedside lamp, "
                "and a chair by the window."
            )
        else:
            print(
                "Two identical beds stand in the room now, each with a bedside lamp. "
                "You cannot remember where the second one came from."
            )

    def describe_current_location(self) -> None:
        current_location = self.game_map.get_location(self.current_location_id)
        if current_location is not None:
            if self.current_location_id == "room_409":
                self.describe_room_409()
            else:
                current_location.describe()
            current_location.display_connections()
            self.check_location_events()

    def trigger_room_409_bad_ending(self) -> None:
        print("The door clicks shut behind you.")
        print("For a moment, you hear sheets being pulled tight on two beds.")
        print()
        print("At the end of the corridor, the Staff Room door is gone.")
        print("In its place is Room 409.")
        print()
        print("A cleaning cart waits outside the door.")
        print("A clipboard rests on top of it.")
        print()
        print("Room 409 — Completed: 01:17 AM")
        print("Signature: You")
        print()
        print("Below it, a new line has been added.")
        print("Room 409 — Scheduled: 01:00 AM")
        print("Assigned employee: You")
        print()
        print('The intercom crackles: "Housekeeping to Room 409."')
        print("The night shift continues.")

    def take_turn(self) -> bool:
        current_location = self.game_map.get_location(self.current_location_id)
        self.describe_current_location()
        command = input("What do you want to do next?").strip()
        if command == "quit":
            return False
        if command == "interact":
            self.interact()
            return True
        if command == "rules":
            if not self.has_rule_book:
                print("You don't have the handbook yet. ")
            else:
                self.rule_book.display_all_rules()
            return True
        parts = command.split()
        if parts and parts[0] == "rule":
            if len(parts) != 2:
                print(
                    "Invalid command. Please use 'rules' to see all rules or "
                    "'rule <rule_id>' to see a specific rule."
                )
            elif not self.has_rule_book:
                print("You don't have the handbook yet. ")
            else:
                self.rule_book.display_rule(parts[1])
            return True
        if command == "room_409" and self.room_409_locked:
            print("The door to Room 409 will not open.")
            return True
        if self.move_to(command):
            print(f"You move to {command}")
            if self.hallucinating:
                self.trigger_room_409_bad_ending()
                return False
            if self.current_location_id == "reception" and self.room_409_visits >= 1:
                self.trigger_handover_ending()
                return False
            self.describe_current_location()
            return True
        if self.game_map.get_location(command) is None:
            print(f"Location '{command}' does not exist.")
        else:
            print(f"You cannot go to '{command}' from your current location.")
        if current_location is not None:
            current_location.display_connections()
        return True

    def run(self) -> None:
        print("Welcome to the Grante Hotel!")
        keep_playing = True
        while keep_playing:
            keep_playing = self.take_turn()
        if not keep_playing:
            print("Game over.")
