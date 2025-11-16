class ValidationError(Exception):
    """
    Користувацька помилка валідації для бізнес-логіки (не Pydantic).
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
