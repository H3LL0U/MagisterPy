class BaseMagisterError(Exception):
    
    def __init__(self, message=None):
        super().__init__(message)
        self.message = message


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
class AuthcodeError(BaseMagisterError):
    def __init__(self, message="\nCould not get the authcode from the javascript. This is likely due to magister updating their code structure, please update the package or create an issue if it the latest version"):
        super().__init__(message)
        self.message = message