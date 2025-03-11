import requests
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from .jsparser import *
from typing import Optional


class LoginRequestsSender():

    def __init__(self):
        pass

    def get_subdomain(self, url):

        parsed_url = urlparse(url)

        netloc = parsed_url.netloc

        parts = netloc.split('.')

        if len(parts) > 2:

            return '.'.join(parts[:-2])
        else:
            return None

    def get_accountid(self, request_session: requests.Session, app_auth_token, api_url) -> str:
        url = f"{api_url}/sessions/current"

        headers = {
            "authorization": app_auth_token
        }
        response = request_session.get(
            url, headers=headers, cookies=request_session.cookies)
        if response.status_code == 200:
            response_link = response.json()["links"]["account"]["href"]
            account_id = response_link[response_link.rfind("/")+1:]

            return account_id

    def get_personid(self, request_session: requests.Session, app_auth_token, api_url, account_id) -> str:

        url = f"{api_url}/accounts/{account_id}"

        headers = {
            "authorization": app_auth_token
        }

        response = request_session.get(url=url, headers=headers)

        if response.status_code == 200:
            response_link = response.json()["links"]["leerling"]["href"]
            personid = response_link[response_link.rfind("/")+1:]

            return personid

    def extract_auth_token(self, url) -> str:
        # Parse the URL to get the fragment
        parsed_url = urlparse(url)

        fragment = parsed_url.fragment

        # Parse the fragment to get the id_token
        token_params = parse_qs(fragment)
        id_token = token_params.get('access_token')

        if id_token:
            return id_token[0]  # Return the first id_token found
        else:
            return None

    def get_profile_auth_token(self, request_session: requests.Session) -> str:
        url = r"https://accounts.magister.net/connect/authorize?client_id=iam-profile&redirect_uri=https%3A%2F%2Faccounts.magister.net%2Fprofile%2Foidc%2Fredirect_callback.html&response_type=id_token%20token&scope=openid%20profile%20email%20magister.iam.profile&state=57dcb9c3b667407791ff32a7af41e703&nonce=ec78d557c0e44751bf573db6719445cd"
        response = request_session.get(url, allow_redirects=False)

        url = response.headers["Location"]
        return "Bearer " + self.extract_auth_token(url)

    def get_app_auth_token(self, request_session: requests.Session, api_url) -> str:
        url = "https://accounts.magister.net/connect/authorize"
        subdomain = self.get_subdomain(api_url)
        # Parameters as a dictionary
        params = {
            # might cause problems if subdomains for other schools are implemented differently TODO: Implement a system that reads https://{subdomain}.magister.net/oidc_config.js to get the string added to the domain at the client_id field
            "client_id": f"M6-{subdomain}.magister.net",
            "redirect_uri": f"https://{subdomain}.magister.net/oidc/redirect_callback.html",
            "response_type": "id_token token",
            "scope": "openid profile opp.read opp.manage attendance.overview attendance.administration "
            "calendar.user calendar.ical.user calendar.to-do.user grades.read grades.manage "
            "oso.administration registration.admin lockers.administration enrollment.admin",
            "state": "57dcb9c3b667407791ff32a7af41e703",
            "nonce": "ec78d557c0e44751bf573db6719445cd",
            "acr_values": f"tenant:{subdomain}.magister.net"
        }

        response = request_session.get(
            url, params=params, allow_redirects=False)
        url = response.headers["Location"]
        return "Bearer " + self.extract_auth_token(url)

    def get_api_url(self, request_session: requests.Session, profile_auth_token) -> str:
        headers = {"authorization": profile_auth_token}

        response = request_session.get(
            "https://magister.net/.well-known/host-meta.json", headers=headers)

        items = response.json()
        main_page = items["links"][0]["href"]
        return main_page

    def search_for_tenant_id(self, request_session: requests.Session, school_name, session_id) -> str:
        response = request_session.get(
            f"https://accounts.magister.net/challenges/tenant/search?sessionId={session_id}&key={school_name}")
        return response.json()[0]["id"]

    def set_school(self, request_session: requests.Session, school_name, main_payload) -> requests.Response:

        tenant_id = self.search_for_tenant_id(
            request_session, school_name, main_payload["sessionId"])
        main_payload["tenant"] = tenant_id

        response = self.send_post_request(
            request_session, main_payload, "https://accounts.magister.net/challenges/tenant")
        return response

    def set_password(self, request_session, password, main_payload) -> requests.Response:
        main_payload["password"] = password
        main_payload["userWantsToPairSoftToken"] = False
        return self.send_post_request(request_session, main_payload, "https://accounts.magister.net/challenges/password")

    def set_username(self, request_session, username, main_payload) -> requests.Response:

        main_payload["username"] = username
        response = self.send_post_request(
            request_session, main_payload, "https://accounts.magister.net/challenges/username")
        return response

    def send_post_request(self, request_session: requests.Session, payload, url, auth_token=None) -> requests.Response:

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": auth_token,
            "origin": "https://accounts.magister.net",
            "x-xsrf-token": request_session.cookies.get("XSRF-TOKEN")
        }

        response = request_session.post(
            url=url, json=payload, headers=headers, cookies=request_session.cookies)
        return response

    def extract_redirect_url_from_html(self, html_content: str) -> str:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the script tag with defer attribute
        script_tag = soup.find('script', {'defer': 'defer'})

        # Extract the src attribute
        if script_tag and 'src' in script_tag.attrs:
            script_src = script_tag['src']
            return script_src
        else:
            return None

    def extract_dynamic_authcode(self, js_content):
        return JsParser().get_authcode_from_js(js_content=js_content)
