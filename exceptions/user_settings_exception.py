
class UserSettingsException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'UserSettingsException, {0}'.format(self.message)
        else:
            return 'UserSettingsException'

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