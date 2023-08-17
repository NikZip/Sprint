class StatusIsNotNewException(Exception):
    """Raised when trying to edit Pass with status that is not new"""
    def __init__(self, status):
        message = f"Cannot modify passes that is not new. The current status is '{status}'."
        super().__init__(message)

