import concurrent.futures

from requests_oauthlib import OAuth2Session
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.headless = True
opts.add_argument('--no-sandbox')
assert opts.headless  # Operating in headless mode

from offstack.managers import oAuthManager, DriverManager

class LoginPresenter:
    def __init__(self, queue, login_service):
        self.queue = queue
        self.login_service = login_service


    def on_initialize_profile(self, **kwargs):
        print("in presenter: ", kwargs)
        self.queue.put(dict(action="hide"))
# def save_access_token(interface, Firefox, browser_opts, email, password, queue, gtk): 
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         params_dict = {
#             "email": email,
#             "password": password
#         }
#         future = executor.submit(create_user_file, email, password)
#         return_value = future.result()

#         if not return_value:
#             print("Could not save to file")
#             return

#         browser = Firefox(options=opts)
#         oauth_manager = oAuthManager(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, OAuth2Session, SCOPE)
#         oauth_manager.create_session()
#         driver = DriverManager(CLIENT_ID, CLIENT_SECRET, browser)
#         user_data = email, password
#         response = request_access_token(driver, oauth_manager, user_data)
#         queue.put({"create_user": {"response":response}})
#         # if response:
#         #     obj.idle_add(display_dashboard, interface, OAuth2Session, Firefox, browser_opts, queue, gtk)
#         #     login_window = interface.get_object("LoginWindow")
#         #     login_window.hide()

