class BaseApplicationException(Exception):
    def __init__(
            self,
            message: str,
            code: str
            ):
        self.message = message
        self.code = code
        super().__init__(self.message)

    def to_dict(self):
        """
        Converts the exception to a dictionary for a structured API response.
        """
        error_dict = {
            "status": "error",
            "error": {
                "code": self.code,
                "message": self.message
            }
        }
        # Add details if available
        if hasattr(self, 'detail') and self.detail:
            error_dict["error"]["details"] = self.detail
        return error_dict