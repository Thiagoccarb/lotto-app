import re

class StatusError(Exception):
    def __init__(
        self, message: str, status_code: int = 400, status: str = None, **kwargs
    ):
        formats = re.findall(r"{(.*?)}", message)
        message = message.format(**{fmt: kwargs[fmt] for fmt in formats})
        self.message = message
        self.status_code = status_code
        self.status = status
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__(message)


class NotFoundError(StatusError):
    def __init__(self):
        super().__init__(
            message="Resource not found.", status_code=404, status="not_found"
        )
