import time
import concurrent.futures
from threading import Thread

from .managers import oAuthManager, DriverManager
from .utils import request_access_token, check_user_credentials
from .logger import logger
from .constants import (
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI,
    SCOPE,
    VERSION,
    USERDATA
)

class LoginHandlers:
    def __init__(self, interface, OAuth2Session, Firefox, browser_opts, queue):
        self.interface = interface
        self.OAuth2Session = OAuth2Session
        self.Firefox = Firefox
        self.browser_opts = browser_opts
        self.queue = queue

    def login_button_clicked(self, button):
        email = self.interface.get_object('login_username_entry').get_text().strip()
        password = self.interface.get_object('password_username_entry').get_text().strip()

        message_dialog = self.interface.get_object("MessageDialog")
        dialog_title = self.interface.get_object("dialog_title")
        primary_text_title = self.interface.get_object("primary_text_title")

        dialog_title.set_text("Intializing profile")  
        primary_text_title.set_text("Saving credentials and getting access token...")  

        message_dialog.show()

        if not len(email) == 0 and not len(password) == 0:          
            thread = Thread(target=save_access_token, args=[self.interface, self.Firefox, self.browser_opts, self.OAuth2Session, email, password, self.queue])
            thread.daemon = True
            thread.start()
        else:
            print("some of the fields were left empty")

    def need_help_login_label_clicked(self, label, link):
        popover = self.interface.get_object("need_help_popover_menu")
        popover.show()

def save_access_token(interface, Firefox, browser_opts, OAuth2Session, email, password, queue): 
    with concurrent.futures.ThreadPoolExecutor() as executor:
        params_dict = {
            "email": email,
            "password": password
        }
        future = executor.submit(create_user_file, email, password)
        return_value = future.result()

        if not return_value:
            print("Could not save to file")
            return

        browser = Firefox(options=browser_opts)
        oauth_manager = oAuthManager(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, OAuth2Session, SCOPE)
        oauth_manager.create_session()
        driver = DriverManager(CLIENT_ID, CLIENT_SECRET, browser)
        user_data = email, password
        queue.put({"create_user": {"response":request_access_token(driver, oauth_manager, user_data)}})

def create_user_file(email, password):
    try:
        with open(USERDATA, 'w') as f:
            f.write("{0}\n{1}".format(email, password))
            print()
            print("User data saved to file!")
            logger.debug("User data saved to file!")
            return True
    except:
        return False
