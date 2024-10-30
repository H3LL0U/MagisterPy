from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver as wire_webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import logging
class MagistersSession():
    def __init__(self, timeout_per_request = 15):
        self.login_cookies = None
        self.auth_token = None
        self.person_id = None
        self.school_name = None
        self.school_domain = None
        self.session_id = None
        self.enable_log = True
        self.timeout = timeout_per_request
        
    def authorize(self, school_name,school_domain,username,password):
        uri = "https://accounts.magister.net/profile/"
        self.school_name = school_name
        self.school_domain = school_domain
        # Configure Chrome options
        
        logging.getLogger('seleniumwire').setLevel(logging.WARNING)
        options = Options()
        options.add_argument("--log-level=3")
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--blink-settings=imagesEnabled=false")  # Disable images

        # Create a Selenium Wire WebDriver
        #driver = wire_webdriver.Chrome()
        driver = driver = wire_webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, self.timeout)
        driver.get(uri)
        
        school_input = wait.until(EC.presence_of_element_located((By.ID, "scholenkiezer_value")))
        
        school_input.send_keys(school_name)
        
        time.sleep(1)
        school_input.send_keys(Keys.RETURN)

            # Step 2: Input the username and wait for the username field to appear
        
        username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_input.send_keys(username)
        time.sleep(1)
        username_input.send_keys(Keys.RETURN)

            # Step 3: Input the password and wait for the password field to appear

        
        password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(1)
        wait.until(EC.url_contains("https://accounts.magister.net/profile/#/"))
        
        driver.get(f"https://{school_domain}.magister.net/magister/#/vandaag")
        # Navigate to the specified URL
        
        
        # Allow some time for the requests to complete
        wait.until(EC.url_contains(f"https://{school_domain}.magister.net/magister/#/vandaag"))
        

        # Intercept requests and check for the Bearer token
        for request in driver.requests[::-1]:
            
            if request.response and 'Authorization' in request.headers:
                value = request.headers['Authorization']
                if value.startswith('Bearer'):
                    
                    self.auth_token = value
                    
                    self.log(f"\nauth token found!")
                    break
                    
                    
        self.login_cookies = driver.get_cookies()
        

        # Clean up
        if self.set_session_id():
            self.log("session id set!")
        if self.set_person_id():
            self.log(f"person id set!{self.person_id}")
        driver.quit()

        self.log("Authorization successful!")
    #def get_json_for_date
    def set_session_id(self):
        '''
        returns true if the id session was set returns False if not
        '''
        if self.login_cookies:
            for cookie in self.login_cookies:
                if cookie["name"] == "idsrv.session":
                    self.session_id = cookie["value"]
                    return True
        
        return False
    def get_school_rooster(self,_from,to):
        if not(self.person_id and self.auth_token):
            self.log("Session not authorized. Please authorize first before using the functions")
            return None
        url = f"https://o2groningen.magister.net/api/personen/{self.person_id}/afspraken"
        params = {
            "status": "1",
            "tot": _from, #2024-11-08
            "van": to#"2024-11-01"
        }
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US;q=0.8,en;q=0.7,nl;q=0.6",
            "authorization": f"{self.auth_token}",
            #"cookie": f"SESSION_ID={self.session_id}",
            "priority": "u=1, i",
            "referer": "https://o2groningen.magister.net/magister/",
            "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"
        }
    
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            self.log("Request was successful!")
            return response.json()  # If JSON response is expected
        else:
            self.log(f"Request failed with status code {response.status_code}")
            return response.json()["Items"]
    def set_person_id(self):
        url = f"https://{self.school_domain}.magister.net:443/api/toestemmingen"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US;q=0.8,en;q=0.7,nl;q=0.6",
            "authorization": f"{self.auth_token}",
            "cookie": f"SESSION_ID={self.session_id}",
            "priority": "u=1, i",
            "referer": "https://o2groningen.magister.net/magister/",
            "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"
        }
        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            
            self.person_id = request.json()["items"][0]["persoonId"]
            return True
        
        
        return False
        

    def log(self,msg):
        if self.enable_log:
            print(msg)

    








