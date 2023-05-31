class APIException(Exception):
    def __init__(self, message, status_code):
        super(APIException, self).__init__(message)
        self.status_code = status_code
