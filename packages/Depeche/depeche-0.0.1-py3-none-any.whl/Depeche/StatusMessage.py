import uuid

class StatusMessage:
    """Represents a status message."""
    def __init__(self, message: str):
        self.id = uuid.uuid4()  # Unique ID
        self.message = message
        self.stale = False  # Initially set to False

    def mark_stale(self):
        """Mark message as stale."""
        self.stale = True
