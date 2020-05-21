from requests_oauthlib import OAuth2Session
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.headless = True
opts.add_argument('--no-sandbox')
assert opts.headless  # Operating in headless mode

import html2text
from offstack.managers import oAuthManager, DriverManager
from offstack.services.request_service import RequestService
from offstack.logger import logger
from offstack.utils import (
    check_access_token,
    get_user_credentials,
    get_questions,
    display_favorite_question
)

from offstack.constants import(
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI,
    SCOPE,
    USERDATA,
    CURRDIR,
)

class DashboardPresenter(RequestService):
    def __init__(self, queue):
        self.queue = queue
    
    def load_content(self, question_id, question_textview, answers_textview):
        question, resp_count, answers = display_favorite_question(question_id)
        

        question_string = html2text.html2text(question)
        question_buffer = question_textview.get_buffer()
        question_buffer.set_text(question_string)

        answer_string = html2text.html2text(answers)
        answers_buffer = answers_textview.get_buffer()
        answers_buffer.set_text(answer_string)

    def cache_favorites(self):
        logger.debug("Creating oAuth Session")
        oauth_manager = oAuthManager(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, OAuth2Session, SCOPE)
        oauth_manager.create_session()
        if not check_access_token():
            browser = Firefox(options=opts)

            driver = DriverManager(CLIENT_ID, CLIENT_SECRET, browser)

            user_data = get_user_credentials()

            resp = RequestService.request_access_token(driver, oauth_manager, user_data)
            if not resp:
                print("Unable to get the access token.")
                return
        
        if RequestService.request_favorites(oauth_manager):
            return get_questions()
        else:
            return False

    def populate_on_load(self, questions_list_store):
        questions_list = get_questions()
        
        if not questions_list:
            questions_list = self.cache_favorites()

        questions_list_store.clear()
        
        for question in questions_list:
            tags = '; '.join(question["tags"])
            questions_list_store.append([question["question_id"], question["title"], "Yes" if question["score"] else "No", str(question["score"]), tags])
