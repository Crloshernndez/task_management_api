class BaseApplicationException:
    def __init__(
            self,
            message: str,
            detail: str,
            code: str
            ):
        self.message = message
        self.detail = detail
        self.code = code
        super().__init__(self.message)

    def to_dict(self):
        """
        Converts the exception to a dictionary for a structured API response.
        """
        return {
            "status": "error",
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.detail
            }
        }