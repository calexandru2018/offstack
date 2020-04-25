
from .managers import oAuthManager, DriverManager
from offstack.logger import logger
from .utils import (
    check_access_token,
    request_access_token,
    get_user_credentials,
    request_favorites,
    get_questions,
    display_favorite
)

from .constants import(
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI,
    SCOPE,
    USERDATA,
    CURRDIR
)

def display_dashboard(interface, OAuth2Session, Firefox, opts, queue):
    interface.add_from_file(CURRDIR+"/resources/dashboard_window.glade")
    dashboard_window = interface.get_object("DashboardWindow")
    interface.connect_signals(DashboardHandlers(interface, OAuth2Session, Firefox, opts, queue))

    dashboard_window.show()

class DashboardHandlers():
    def __init__(self, interface, OAuth2Session, Firefox, browser_opts, queue):
        self.interface = interface
        self.OAuth2Session = OAuth2Session
        self.Firefox = Firefox
        self.browser_opts = browser_opts
        self.queue = queue
        populate_on_load(self.interface, self.OAuth2Session, self.Firefox, self.browser_opts, self.queue)

    def search_entry_key_release_event(self, entry, event):
        print("Filter")

    
def cache_favorites(interface, OAuth2Session, Firefox, browser_opts, queue):
    logger.debug("Creating oAuth Session")
    oauth_manager = oAuthManager(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, OAuth2Session, SCOPE)
    oauth_manager.create_session()
    if not check_access_token():
        browser = Firefox(options=browser_opts)

        driver = DriverManager(CLIENT_ID, CLIENT_SECRET, browser)

        user_data = get_user_credentials()

        resp = request_access_token(driver, oauth_manager, user_data)
        if not resp:
            print("Unable to get the access token.")
            return
    
    if request_favorites(oauth_manager):
        return get_questions()
    else:
        return False

def populate_on_load(interface, OAuth2Session, Firefox, browser_opts, queue):
    questions_list = get_questions()
    questions_list_store = interface.get_object("QuestionsListStore")
    
    if not questions_list:
        questions_list = cache_favorites(interface, OAuth2Session, Firefox, browser_opts, queue)

    questions_list_store.clear()
    for question in questions_list:
        tags = '; '.join(question["tags"])
        questions_list_store.append([question["question_id"], question["title"], "Yes" if question["score"] else "No", str(question["score"]), tags])