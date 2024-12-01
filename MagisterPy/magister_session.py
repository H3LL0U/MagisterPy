import requests
from urllib.parse import urlparse, parse_qs
from .request_manager import LoginRequestsSender
from typing import Optional
from .error_handler import error_handler
from .magister_errors import *

class MagisterSession():
    '''
    Creates a session with Magister

    Parameters:
            enable_logging (bool):  Used to display errors in the standard output

            automatically_handle_errors (bool): Used to automatically handle errors. If any function fails it returns None instead of raising an error
    '''

    def __init__(self, enable_logging = False, automatically_handle_errors = True):

        self.request_sender = LoginRequestsSender()
        self.session = requests.Session()
        self.profile_auth_token = None #auth token for the redirect page
        self.app_auth_token = None #auth token for the main app
        self.authcode = None # gets randomly generated once every 3-7 days
        self.sessionid = None # gets assigned when entering the login page
        self.returnurl = None # used for some requests
        self.main_payload = None #payload containing common parameters (authcode, returnurl, sessionid)
        self.person_id = None # your account's person_id
        self.account_id = None #your account id
        self.api_url = None #url for accessing magister API
        self.x_correlation_id = None #used in login requests
        self.automatically_handle_errors = automatically_handle_errors

        self.recieve_log = enable_logging
    def _logMessage(self,msg:str):
        if self.recieve_log:
            print(msg)
    

    @error_handler
    def input_school(self, school_name:str) ->Optional[requests.Response]:
        '''
        Sets up a session by inputting the school name. This is the **first step** in the login sequence 
        and must be called before `input_username()` and `input_password()`.

        Parameters:
            school_name (str): The name of the school to authenticate against.

        Usage:
            This method is the **first step** of the login process. It must be called before 
            `input_username()` and `input_password()` to initialize the session.

        Returns:
            requests.Response: if the school is found and session is successfully initiated.
            None: if the school is not found or there’s an issue in the school lookup.

        Example:
            session.input_school("MySchoolName")
        '''


        #Initializing the login session
        url_login_page = "https://accounts.magister.net/"

        response = self.session.get(url_login_page,allow_redirects=False)

        redirect_url_1 = r"https://accounts.magister.net/connect/authorize?client_id=iam-profile&redirect_uri=https%3A%2F%2Faccounts.magister.net%2Fprofile%2Foidc%2Fredirect_callback.html&response_type=id_token%20token&scope=openid%20profile%20email%20magister.iam.profile&state=57dcb9c3b667407791ff32a7af41e703&nonce=ec78d557c0e44751bf573db6719445cd"
        response = self.session.get(redirect_url_1,allow_redirects=False)

        
        response = self.session.get(response.headers.get("location"), allow_redirects= False)
        
        response = self.session.get("https://accounts.magister.net/" + response.headers.get("location"), allow_redirects= False)
        
        self.sessionid = parse_qs(urlparse(response.url).query).get('sessionId', [None])[0]
        self.returnurl = parse_qs(urlparse(response.url).query).get('returnUrl', [None])[0]
        self.x_correlation_id = parse_qs(urlparse(self.returnurl).query).get('X-Correlation-ID', [None])[0]

        javascript_redirect_url = self.request_sender.extract_redirect_url_from_html(response.text)
        
        
        response = self.session.get(f"https://accounts.magister.net/{javascript_redirect_url}")
        
        self.authcode = self.request_sender.extract_dynamic_authcode(response.text)
        
        

        self.main_payload = {
        'authCode': self.authcode,
        'returnUrl': self.returnurl, 
        'sessionId': self.sessionid
        }
        #Inputting the credentials

        #school
        try:
            response = self.request_sender.set_school(request_session=self.session,school_name=school_name,main_payload=self.main_payload)
            if response.status_code !=200:
                raise IncorrectCredentials(f"Could not find school: {school_name}")
        except requests.exceptions.JSONDecodeError:
            raise IncorrectCredentials(f"Could not find school: {school_name}")
            
        return response
    @error_handler
    def input_username(self,username:str) -> Optional[requests.Response]:
        '''
    Sets the username for the current session. This is the **second step** in the login sequence 
    and must be called after `input_school()` but before `input_password()`.

    Parameters:
        username (str): The username for the account.

    Usage:
        This function must be called **after `input_school()`** and **before `input_password()`** to 
        authenticate the username.

    Returns:
        requests.Response: if the username is accepted.
        None: if the username is not found or if there’s an issue during authentication.

    Example:
        session.input_username("myusername")
    '''

        if not self.main_payload:
            raise UnableToInputCredentials()
        response = self.request_sender.set_username(request_session=self.session,username=username,main_payload=self.main_payload)
        if response.status_code != 200:
            raise IncorrectCredentials()
            
        
        return response
    @error_handler
    def input_password(self,password:str) -> Optional[requests.Response]:
        '''
        Sets the password for the session and finalizes the login process. This is the **third and final step** 
        in the login sequence and must be called after `input_school()` and `input_username()`.

        Upon success, this method retrieves and stores essential session variables like `profile_auth_token`, 
        `api_url`, `app_auth_token`, `account_id`, and `person_id` for further interactions with the API.

        Parameters:
            password (str): The password associated with the username.

        Usage:
            This function is the **final step** in the login process and should only be called **after 
            `input_school()` and `input_username()`**.

        Returns:
            requests.Response: if the password is correct and login is successful.
            None: if the password is incorrect or if there’s a login cooldown.

        Example:
            session.input_password("mypassword")
        '''
        if not self.main_payload:
            raise UnableToInputCredentials()
        response = self.request_sender.set_password(request_session=self.session,password=password,main_payload=self.main_payload)
        if response.status_code !=200:
            raise IncorrectCredentials("Incorrect password or the password input is on cooldown")
            
        #setup for variables
        self.profile_auth_token = self.request_sender.get_profile_auth_token(request_session=self.session)
        self.api_url = self.request_sender.get_api_url(request_session=self.session,profile_auth_token=self.profile_auth_token)
        self.app_auth_token = self.request_sender.get_app_auth_token(request_session=self.session,api_url=self.api_url)
        self.account_id = self.request_sender.get_accountid(request_session=self.session,app_auth_token=self.app_auth_token,api_url=self.api_url)
        self.person_id = self.request_sender.get_personid(request_session=self.session,app_auth_token=self.app_auth_token,api_url=self.api_url,account_id=self.account_id)

        self._logMessage("you have successfully logged in!")
        return response
    @error_handler
    def login(self,school_name:str,username:str,password:str) -> bool:
        '''
        logs the user into their account

        returns:
        True -> if user logged in successfully
        False -> if user wasn't able to login

        params:
        school_name -> a string of school name (not case sensitive. It sets the first school from the list that magister provides)
        username -> a string of a username (should be exact)
        password -> a string with the password of the user (should be exact)
        '''
        #Inputting the school
        input_school_response = self.input_school(school_name=school_name)
        
        if not input_school_response:
            return False
            

        #username
        input_username_response = self.input_username(username=username)
        if not input_username_response:
            return False
        #password
        input_password_response = self.input_password(password=password)
        if not input_password_response:
            return False
        
        return True


    @error_handler
    def get_schedule(self, _from:str, to:str,with_changes = False) -> list[dict]:
        '''
    Retrieves the user’s schedule within a specified date range.
    
    This method fetches all scheduled items between two dates, starting from `_from` to `to`.
    The session must be authenticated by calling `.login()` first.

    Parameters:
    - _from (str): Start date of the schedule period in "YYYY-MM-DD" format.
    - to (str): End date of the schedule period in "YYYY-MM-DD" format.
    - with_changes: Sends a different requests which retrieves recent changes. (It's not getting the changes on specific dates specifically so it's recomended to use with_changes = False instead)
    Returns:
    - list[dict]: A list of dictionaries representing schedule items, each with detailed fields. 
      The schedule items are sorted chronologically from earliest to latest.

    Structure of Each Schedule Item:
    ```json
    {
        "Start": "datetime",                   # Start time of the scheduled item
        "Einde": "datetime",                   # End time of the scheduled item
        "LesuurVan": bool,                     # Boolean for lesson period start
        "LesuurTotMet": bool,                  # Boolean for lesson period end
        "DuurtHeleDag": bool,                  # Whether the event lasts all day
        "Omschrijving": str,                   # Description of the event
        "Lokatie": str,                        # Location of the event
        "Status": int,                         # Status code of the event
        "Type": int,                           # Type identifier of the event
        "Subtype": int,                        # Subtype identifier of the event
        "IsOnlineDeelname": bool,              # Whether online attendance is allowed
        "WeergaveType": int,                   # Display type identifier
        "Inhoud": str,                         # Content or details about the event
        "Opmerking": str,                      # Additional notes
        "InfoType": int,                       # Information type identifier
        "Aantekening": str,                    # Notes or annotations
        "Afgerond": bool,                      # Whether the event is completed
        "HerhaalStatus": int,                  # Repeat status identifier
        "Herhaling": None,                     # Repeat information (usually null)
        "Vakken": list[dict],                  # List of subjects related to the event
        "Docenten": list[dict],                # List of teachers associated with the event
        "Lokalen": list[dict],                 # List of rooms assigned for the event
        "Groepen": None,                       # Group information (usually null)
        "OpdrachtId": int,                     # Task ID if associated
        "HeeftBijlagen": bool,                 # Whether attachments are available
        "Bijlagen": None                       # Attachment information (usually null)
    }
    ```

    Example Usage:
    ```python
    session.get_schedule(_from="2024-11-10", to="2024-11-11")
    ```
    '''
        if not self.app_auth_token:
            self._logMessage("You have not logged in yet")
            return
        #Returns a schedule with no changes in it
        remove_links_and_id = lambda a: {k: v for k, v in a.items() if k not in ["Links", "Id"]}
        params = {
            "status" : 1,
            "tot": to,
            "van": _from
            }
        headers = {"authorization":self.app_auth_token}
        if not with_changes:
            

            
            url = f"{self.api_url}/personen/{self.person_id}/afspraken"
            respone = self.session.get(url=url,params=params,headers=headers)


        else:
            del params["status"]
            url = f"{self.api_url}/personen/{self.person_id}/roosterwijzigingen"
            respone = self.session.get(url=url,params=params,headers=headers)
            
        if respone.status_code == 200:

            response_json = respone.json()["Items"]
            return list(map(remove_links_and_id,response_json))
    @error_handler
    def get_grades(self, top:int = 25,skip:int = 0) -> list[dict]:
        '''
    Retrieves the most recent grades for the user.
    
    This method fetches the latest grades for the authenticated user.
    The session must be authenticated by calling `.login()` first.

    Parameters:
    - top (int): Number of grades to retrieve (default is 25).
    - skip (int): Number of grades to skip, for pagination (default is 0).

    Returns:
    - list[dict]: A list of dictionaries, each representing a grade item with relevant details. 
      Grades are sorted from the most recent to the oldest.

    Structure of Each Grade Item:
    ```json
    {
        "omschrijving": str,                  # Description of the grade item
        "ingevoerdOp": "datetime",            # Date when the grade was entered
        "vak": {                              # Subject information
            "code": str,                      # Subject code
            "omschrijving": str               # Subject description
        },
        "waarde": str,                        # Grade value or score
        "weegfactor": float,                  # Weight factor of the grade
        "isVoldoende": bool,                  # Whether the grade is sufficient
        "teltMee": bool,                      # Whether the grade counts in the final score
        "moetInhalen": bool,                  # If the grade needs to be retaken
        "heeftVrijstelling": bool,            # If the grade has an exemption
        "behaaldOp": None,                    # Date achieved (if available)
        "links": dict                         # Additional links or references (usually empty)
    }
    ```

    Example Usage:
    ```python
    session.get_grades(top=1)
    ```
    '''
        if not self.app_auth_token:
            self._logMessage("You have not logged in yet")
            return
        remove_id = lambda a: {k: v for k, v in a.items() if k not in ["kolomId"]}
        params = {
        "top": top,
        "skip": skip
        }
        headers = {"authorization":self.app_auth_token}
        url = f"{self.api_url}/personen/{self.person_id}/cijfers/laatste"
        respone = self.session.get(url=url,params=params,headers=headers)

        if respone.status_code == 200:

            response_json = respone.json()["items"]
            return list(map(remove_id,response_json))
        
