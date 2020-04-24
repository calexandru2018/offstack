from requests_oauthlib import OAuth2Session

from offstack.managers import oAuthManager, DriverManager
from offstack.utils import request_access_token
from offstack.logger import logger

from .constants import (
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI,
    SCOPE,
    VERSION,
    USERDATA
)

class LoginHandlers:
    def __init__(self, interface, Firefox, browser_opts):
        self.interface = interface
        self.Firefox = Firefox
        self.browser_opts = browser_opts

    def login_button_clicked(self, button):
        # login_username_entry
        # password_username_entry
        email = self.interface.get_object('login_username_entry').get_text().strip()
        password = self.interface.get_object('password_username_entry').get_text().strip()

        if not len(email) == 0 and not len(password) == 0:
            with open(USERDATA, 'w') as f:
                f.write("{0}\n{1}".format(email, password))
                print()
                print("User data saved to file!")
                logger.debug("User data saved to file!")

            browser = self.Firefox(options=self.browser_opts)

            oauth_manager = oAuthManager(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, OAuth2Session, SCOPE)

            oauth_manager.create_session()

            driver = DriverManager(CLIENT_ID, CLIENT_SECRET, browser)

            user_data = [email, password]

            resp = request_access_token(driver, oauth_manager, user_data)

            if resp:
                # self.window = QtWidgets.QMainWindow()
                # self.ui = DashboardWindow()
                # self.ui.setupUi(self.window)
                # self.window.show()
                print("Logged in")
                logger.debug("Displaying Dashboard")
                # LoginWindow.hide()

            else:
                print("Unable to intialize account.\nEither incorrect credentials were providade or there are some connectivity issues.")
                logger.debug("[!] Unable to get acess_token.")
        else:
            print("some of the fields were left empty")