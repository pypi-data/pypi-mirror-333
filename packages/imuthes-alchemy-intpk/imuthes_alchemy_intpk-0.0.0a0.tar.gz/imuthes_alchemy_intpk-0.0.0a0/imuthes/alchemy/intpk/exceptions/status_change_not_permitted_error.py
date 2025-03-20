from ...exceptions import AlchemyException


class StatusChangeNotPermittedError(AlchemyException):
    """Raised when the new status cannot be set."""

    def __init__(self, record, new_status: str):
        self.record = record
        self.new_status = new_status
        super().__init__(f"Changing Status from »{self.record.status.name}« to »{new_status}« not possible.")
        self.log()
