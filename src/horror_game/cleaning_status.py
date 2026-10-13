class RoomCleaningStatus:
    def __init__(self) -> None:
        self.completed_at: str | None = None
        self.signed_by: str | None = None

    def mark_room_409_completed(self) -> None:
        self.completed_at = "01:17 AM"
        self.signed_by = "You"

    def cleaning_schedule_description(self) -> str:
        room_409_completion = self.completed_at or "[blank]"
        return (
            "The cleaning schedule is neatly arranged.\n"
            "Room 408 — Scheduled: 12:30 AM. Completed: 12:42 AM. Signed: M. Lewis.\n"
            "Room 409 — Scheduled: 01:00 AM. Assigned employee: [blank]. "
            f"Completed: {room_409_completion}.\n"
            "Room 410 — Scheduled: 01:30 AM. Completed: 01:41 AM. Signed: R. Cole.\n"
            "The room numbers are orderly, and the paper shows no torn pages or obvious alterations."
        )

    def room_409_cleaning_record_description(self) -> str:
        if self.completed_at is None:
            return (
                "The Room 409 cleaning record is still open. The task has no completion "
                "time and the signature line is blank."
            )

        return (
            "The Room 409 cleaning record is marked completed.\n"
            f"Completed: {self.completed_at}.\n"
            f"Signature: {self.signed_by}."
        )
