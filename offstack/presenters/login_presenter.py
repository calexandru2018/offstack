import concurrent.futures

from requests_oauthlib import OAuth2Session
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.headless = True
opts.add_argument('--no-sandbox')
assert opts.headless  # Operating in headless mode

from offstack.constants import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE
from offstack.managers import oAuthManager, DriverManager
from offstack.services.request_service import RequestService

class LoginPresenter(RequestService):
    def __init__(self, queue, login_service):
        self.queue = queue
        self.login_service = login_service


    def on_initialize_profile(self, **kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")

        if not username or not password:
            self.queue.put(dict(action="update", header="Error", label="Input fields can not be left empty!", spinner=False))
            return False

        if not self.login_service.create_user_file(username, password):
            self.queue.put(dict(action="update", header="Error", label="Unable to save user information to file!", spinner=False))
            return False
        
        if not self.save_access_token():
            self.queue.put(dict(action="update", header="Error", label="Unable to extract token! (It could be related to incorrect credentials)", spinner=False))
            return False
        return True


    def save_access_token(self):
        browser = Firefox(options=opts)
        oauth_manager = oAuthManager(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, OAuth2Session, SCOPE)
        oauth_manager.create_session()
        driver = DriverManager(CLIENT_ID, CLIENT_SECRET, browser)

        response = RequestService.request_access_token(driver, oauth_manager)
        return response

