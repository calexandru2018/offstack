import json
from offstack.logger import logger
from offstack.constants import USERDATA, FAVORITES
from offstack.utils import check_access_token, check_user_credentials

class RequestService:
    # Request access token
    @staticmethod
    def request_access_token(driver, oauth_manager):

        oauth_manager.get_authorization_state_url()

        driver._go_to(oauth_manager.authorization_url)

        with open(USERDATA, 'r') as f:
            user_data = f.readlines()

            print()
            print("Entering user data...")

            user_list_dict = [{'value': user_data[0], "xpath":'//*[@id="email"]'}, {'value': user_data[1], "xpath":'//*[@id="password"]'}]
            driver._type(*user_list_dict)

            driver._click('//*[@id="submit-button"]')
            
            print()
            print("Searching for access token...")

            url = driver._get_current_url()
            print(url)
            driver._quit()

            print()
            print("Extracting access token...")
            logger.debug("Extracting access token.")

            try:
                access_token, state = oauth_manager.extract_state_token(url)
                with open(USERDATA, 'a') as f:
                    f.write("\n{0}".format(access_token))
                    print()
                    print("Access token saved to file.")
                    logger.debug("Access token saved to file.")
            except TypeError:
                print("Unable to extract token! (It could be related to incorrect credentials)")
                logger.debug("[!] Unable to extract token! (It could be related to incorrect credentials or captcha)")
                # sys.exit(1)
                return False

            return True
            
    # Get favorites
    @staticmethod
    def request_favorites(oauth_manager):
        stored_access_token = False
        if not check_access_token():
            if not check_user_credentials():
                print("[!] Unable to request for favorites.")
                logger.debug("[!] Unable to send request favorites.")
                return False

            access_token = request_access_token()
            with open(USERDATA, 'a') as f:
                f.write("\n{0}".format(access_token))
                print()
                print("Access token saved to file.")
                logger.debug("Access token saved to file.")
            
            stored_access_token = access_token

        if not stored_access_token:
            logger.debug("Access token exist, retrieving favorites from file.")
            with open(USERDATA, 'r') as f:
                user_data = f.readlines()
                stored_access_token = user_data[2]

        with open(FAVORITES, 'w') as f:
                json.dump(oauth_manager.fetch_from_api(stored_access_token).json(), f, indent=4)
                print()
                print("Favorites are locally stored!")
                logger.debug("Favorites are locally stored.")
                return True
        