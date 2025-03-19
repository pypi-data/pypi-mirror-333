class InvalidAddressError(Exception):
    pass


class InvalidChainId(Exception):
    pass


class SFError(Exception):

    def __init__(self, type: str, message: str, err: str = None) -> None:
        self.error_message = str(
            {"Type": type, "Message": message, "Error": err})
        super().__init__(self.error_message)
