from PyQt5.QtCore import QThread

class RequestAccessToken(QThread):
    def __init__(self, driver, oauth_manager, user_data, userdata_path):
        QThread.__init__(self)
        self.driver = driver
        self.oauth_manager = oauth_manager
        self.user_data = user_data
        self.userdata_path = userdata_path

    def request_access_token(self):
        self.oauth_manager.get_authorization_state_url()

        self.driver._go_to(self.oauth_manager.authorization_url)

        with open(self.userdata_path, 'r') as f:
            self.user_data = f.readlines()

            print()
            print("Entering user data...")

            user_list_dict = [{'value': self.user_data[0], "xpath":'//*[@id="email"]'}, {'value': self.user_data[1], "xpath":'//*[@id="password"]'}]
            self.driver._type(*user_list_dict)

            self.driver._click('//*[@id="submit-button"]')
            
            print()
            print("Searching for access token...")

            url = self.driver._get_current_url()
            print(url)
            self.driver._quit()

            print()
            print("Extracting access token...")

            try:
                access_token, state = self.oauth_manager.extract_state_token(url)
                with open(self.userdata_path, 'a') as f:
                    f.write("\n{0}".format(access_token))
                    print()
                    print("Access token saved to file.")
                    return True
            except TypeError:
                print("Unable to extract token! (It could be related to incorrect credentials)")
                # sys.exit(1)
                return False

    def __del__(self):
        self.wait()

    def run(self):
       self.request_access_token()