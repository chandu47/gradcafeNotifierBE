
class ResultException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'ProgramResultException, {0}'.format(self.message)
        else:
            return 'ProgramResultException'

class ValidationException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'ValidationException, {0}'.format(self.message)
        else:
            return 'ValidationException'