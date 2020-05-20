from offstack.constants import USERDATA

class LoginService:
    def create_user_file(self, email, password):
        try:
            with open(USERDATA, 'w') as f:
                f.write("{0}\n{1}".format(email, password))
                print()
                print("User data saved to file!")
                # logger.debug("User data saved to file!")
                return True
        except:
            return False