import requests
from .magister_errors import *
def error_handler(func):
    '''
    A decorator used to handle errors that can occure when when executing the functions
    '''
    
    def wrapper(*args, **kwargs):
        _self = args[0]
        try:
            result = func(*args,**kwargs)
            return result
        except KeyboardInterrupt:
            raise KeyboardInterrupt
            
        except requests.exceptions.ConnectionError as e:
            _self._logMessage("Could not connect to Magister")
            if _self.automatically_handle_errors:
                pass
            else:
                raise ConnectionError()
        except BaseMagisterError as e:
            if _self.automatically_handle_errors:
                _self._logMessage(e.message)
            else:
                raise e
    return wrapper