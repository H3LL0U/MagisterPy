class BaseMagisterError(Exception):

    def __init__(self, message=None):
        super().__init__(message)
        self.message = message
        self.msg = message


class UnableToInputCredentials(BaseMagisterError):

    def __init__(self, message="\nCouldn't input the credentials\nThis error can occure if the credentials were not Input in order\nSchool->Username->Passwords"):
        super().__init__(message)
        self.message = message


class IncorrectCredentials(BaseMagisterError):
    def __init__(self, message="\nThe credentials provided were either incorrect or Magister rejected them"):
        super().__init__(message)
        self.message = message


class ConnectionError(BaseMagisterError):
    def __init__(self, message="\nCould not connect to Magister. Please check your internet connection"):
        super().__init__(message)
        self.message = message


class NotLoggedInError(BaseException):
    def __init__(self, message="You were not logged in before running this function"):
        super().__init__(message)
        self.message = message


class AuthcodeError(BaseMagisterError):
    def __init__(self, message="\nCould not get the authcode from the javascript. This is likely due to magister updating their code structure, please update the package or create an issue if it the latest version"):
        super().__init__(message)
        self.message = message


class FetchError(BaseMagisterError):
    def __init__(self, message="\nThere was an error fetching the data. The session has probably expired. Run relogin on the session or enable automatic_relogin through the session parameters."):
        super().__init__(message)
        self.message = message
