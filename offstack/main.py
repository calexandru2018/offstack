import sys

from PyQt5 import QtWidgets
from my_repo.login_window import LoginWindow
from my_repo.dashboard_window import DashboardWindow

from my_repo.utils import check_user_credentials

from my_repo.logger import logger

from my_repo.constants import (
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI,
    SCOPE,
    BASE_API,
    FAVORITES,
    USERDATA, 
    CONFIG_DIR
)


def init():
        
    app = QtWidgets.QApplication(sys.argv)

    if check_user_credentials():
        logger.debug("Displaying Dashboard")
        # call dashboard 
        window = QtWidgets.QMainWindow()
        ui = DashboardWindow()
        ui.setupUi(window)
        window.show()
        sys.exit(app.exec_())
    else:
        logger.debug("Displaying Login")
        # call login
        window = QtWidgets.QMainWindow()
        ui = LoginWindow()
        ui.setupUi(window)
        window.show()
        sys.exit(app.exec_())

    # while True:
    #     print("""
    #     1 - Initialize profile
    #     2 - Save favorites
    #     3 - Show favorites
    #     0 - Exit
    #     """)
    #     print("What would you like to do ?")
    #     inp = input("Choice: ")

    #     try:
    #         int(inp)
    #     except:
    #         print("\n[!] It needs to be a numeric choice.")
    #         continue

    #     if int(inp) == 1:
    #         my_repo.prompt_user_credentials()
    #         continue
    #     elif int(inp) == 2:
    #         my_repo.request_favorites()
    #         continue
    #     elif int(inp) == 3:
    #         my_repo.display_favorites()
    #         continue
    #     elif int(inp) == 0:
    #         print()
    #         print("Exiting my-repo...")
    #         sys.exit(1)
    
if __name__ == '__main__':
	init()