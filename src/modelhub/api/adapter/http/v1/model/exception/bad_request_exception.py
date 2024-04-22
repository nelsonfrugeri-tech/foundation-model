class BadRequestException(Exception):
    def __init__(self, params: list):
        self.params = params

    def get_params(self):
        return self.params
