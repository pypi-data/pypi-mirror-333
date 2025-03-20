class InvalidAuth(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class RequestCrystalPayError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class ErrorWebhook(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

