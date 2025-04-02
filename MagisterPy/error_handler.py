import requests
from .magister_errors import *


def should_start_relogin(_self):
    '''
    returns True if the error was caused outside of the relogin method and automatic relogin is enabled
    '''
    return _self.max_relogin_atempts == _self.relogin_atempts and _self.enable_automatic_relogin


def invoke_relogin(_self):
    if should_start_relogin(_self):
        return _self.relogin()


def error_handler(func, __recursive_call=None):
    '''
    A decorator used to handle errors that can occurre when when executing the methods
    '''
    if __recursive_call is None:
        __recursive_call = False

    def wrapper(*args, **kwargs):
        _self = args[0]
        errors_that_invoke_relogin = [FetchError,
                                      requests.exceptions.ConnectionError]
        try:
            result = func(*args, **kwargs)
            return result
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except (BaseMagisterError, requests.exceptions.ConnectionError) as e:
            # Detects if there is an irregular error in the method and makes sure that the method doesn't rerun recursively
            if any(isinstance(e, error_type) for error_type in errors_that_invoke_relogin) and not __recursive_call and invoke_relogin(_self):

                # Reruns the the method
                return error_handler(func, __recursive_call=True)(*args, **kwargs)

            elif not _self.automatically_handle_errors:
                raise e
            _self._logMessage(str(e))

    return wrapper
