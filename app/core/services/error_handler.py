

class APIException(Exception):
    status_code = 400

    def __init__(self, errors=None, status_code=None):
        Exception.__init__(self)
        if errors is None:
            errors = []
        else:
            for err in errors:
                err["type"] = "LOGICAL"
        if status_code is not None:
            self.status_code = status_code
        self.errors = errors
