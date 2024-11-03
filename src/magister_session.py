import requests
from urllib.parse import urlparse, parse_qs
from request_manager import LoginRequestsSender




class MagisterSession():
    def __init__(self):
        self.request_sender = LoginRequestsSender()
        self.session = requests.Session()
        self.profile_auth_token = None #auth token for the redirect page
        self.app_auth_token = None #auth token for the main app
        self.authcode = "72f0e355703a44e5a9"
        self.sessionid = None
        self.returnurl = None
        self.main_payload = None
        self.person_id = None
        self.account_id = None
        self.api_url = None


        self.recieve_log = True
    def _logMessage(self,msg:str):
        if self.recieve_log:
            print(msg)

    def login(self,school_name,username,password):
        
        url_login_page = "https://accounts.magister.net/"



        response = self.session.get(url_login_page,allow_redirects=False)




        redirect_url_1 = r"https://accounts.magister.net/connect/authorize?client_id=iam-profile&redirect_uri=https%3A%2F%2Faccounts.magister.net%2Fprofile%2Foidc%2Fredirect_callback.html&response_type=id_token%20token&scope=openid%20profile%20email%20magister.iam.profile&state=57dcb9c3b667407791ff32a7af41e703&nonce=ec78d557c0e44751bf573db6719445cd"
        response = self.session.get(redirect_url_1,allow_redirects=False)

        response = self.session.get(response.headers.get("location"), allow_redirects= False)




        response = self.session.get("https://accounts.magister.net/" + response.headers.get("location"), allow_redirects= False)

        self.sessionid = parse_qs(urlparse(response.url).query).get('sessionId', [None])[0]
        self.returnurl = parse_qs(urlparse(response.url).query).get('returnUrl', [None])[0]
        self.authcode = "72f0e355703a44e5a9"

        self.main_payload = {
        'authCode': self.authcode,
        'returnUrl': self.returnurl, 
        'sessionId': self.sessionid
        }
        self.request_sender.set_school(request_session=self.session,school_name=school_name,main_payload=self.main_payload)
        self.request_sender.set_username(request_session=self.session,username=username,main_payload=self.main_payload)
        self.request_sender.set_password(request_session=self.session,password=password,main_payload=self.main_payload)


        self.profile_auth_token = self.request_sender.get_profile_auth_token(request_session=self.session)
        self.api_url = self.request_sender.get_api_url(request_session=self.session,profile_auth_token=self.profile_auth_token)
        self.app_auth_token = self.request_sender.get_app_auth_token(request_session=self.session,api_url=self.api_url)


        self.account_id = self.request_sender.get_accountid(request_session=self.session,app_auth_token=self.app_auth_token,api_url=self.api_url)
        self.person_id = self.request_sender.get_personid(request_session=self.session,app_auth_token=self.app_auth_token,api_url=self.api_url,account_id=self.account_id)
        self._logMessage("you have successfully logged in!")

    def get_schedule(self, _from:str, to:str):

        if not self.app_auth_token:
            self._logMessage("You have not logged in yet")
            return

        params = {
        "status" : 1,
        "tot": to,
        "van": _from
        }
        headers = {"authorization":self.app_auth_token}
        url = f"{self.api_url}/personen/{self.person_id}/afspraken"
        respone = self.session.get(url=url,params=params,headers=headers)
        print(url)
        print(respone.text)
        if respone.status_code == 200:
            return respone.json()