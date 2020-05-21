from offstack.constants import USERDATA

class LoginService:
    def create_user_file(self, username, password):
        try:
            with open(USERDATA, 'w') as f:
                f.write("{0}\n{1}".format(username, password))
                print()
                print("User data saved to file!")
                # logger.debug("User data saved to file!")
        except:
            return False
            
        return True