from requests_oauthlib import OAuth2Session

from PyQt5 import QtCore, QtGui, QtWidgets

from my_repo.dialog import App
from my_repo.managers import oAuthManager, DriverManager
from my_repo.dashboard_window import DashboardWindow
from my_repo.logger import logger

from my_repo.threads import RequestAccessToken

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

opts = Options()
opts.headless = True
opts.add_argument('--no-sandbox')

assert opts.headless  # Operating in headless mode

from my_repo.utils import request_access_token

from my_repo.constants import (
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI,
    SCOPE,
    VERSION,
    USERDATA
)
class LoginWindow():

    def load_dashboard(self):
        email = self.lineEmailInput.text().strip()
        password = self.linePasswordInput.text().strip()
        
        if not len(email) == 0 and not len(password) == 0:
            with open(USERDATA, 'w') as f:
                f.write("{0}\n{1}".format(email, password))
                # os.chmod(USERDATA, 0o600)
                print()
                print("User data saved to file!")
                logger.debug("User data saved to file!")

            browser = Firefox(options=opts)

            oauth_manager = oAuthManager(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, OAuth2Session, SCOPE)

            oauth_manager.create_session()

            driver = DriverManager(CLIENT_ID, CLIENT_SECRET, browser)

            user_data = [self.lineEmailInput.text().strip(), self.linePasswordInput.text().strip()]

            # resp = RequestAccessToken(driver, oauth_manager, user_data, USERDATA)
            # resp.start()
            # while resp.isRunning():
            resp = request_access_token(driver, oauth_manager, user_data)

            if resp:
                self.window = QtWidgets.QMainWindow()
                self.ui = DashboardWindow()
                self.ui.setupUi(self.window)
                self.window.show()
                logger.debug("Displaying Dashboard")
                # LoginWindow.hide()

            else:
                App().initUI("information", "Offstack Dialog", "Unable to intialize account.\nEither incorrect credentials were providade or there are some connectivity issues.")
                logger.debug("[!] Unable to get acess_token.")
        else:
            App().initUI("information", "Offstack Dialog", "You can not leave any of the field empty.")
            logger.debug("[!] Some of the fields were left empty.")
        
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(500, 600)
        LoginWindow.setMinimumSize(QtCore.QSize(500, 600))
        LoginWindow.setMaximumSize(QtCore.QSize(500, 600))
        LoginWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        LoginWindow.setDockOptions(QtWidgets.QMainWindow.AllowNestedDocks|QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(70, 290, 361, 171))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEmailInput = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEmailInput.setObjectName("lineEmailInput")
        self.verticalLayout_2.addWidget(self.lineEmailInput)
        self.linePasswordInput = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.linePasswordInput.setInputMethodHints(QtCore.Qt.ImhSensitiveData)
        self.linePasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.linePasswordInput.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.linePasswordInput.setObjectName("linePasswordInput")
        self.verticalLayout_2.addWidget(self.linePasswordInput)
        self.labelTitle = QtWidgets.QLabel(self.centralwidget)
        self.labelTitle.setGeometry(QtCore.QRect(20, 80, 461, 61))
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        self.labelTitle.setFont(font)
        self.labelTitle.setScaledContents(True)
        self.labelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitle.setObjectName("labelTitle")
        self.labelVersion = QtWidgets.QLabel(self.centralwidget)
        self.labelVersion.setGeometry(QtCore.QRect(190, 170, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.labelVersion.setFont(font)
        self.labelVersion.setTextFormat(QtCore.Qt.PlainText)
        self.labelVersion.setAlignment(QtCore.Qt.AlignCenter)
        self.labelVersion.setObjectName("labelVersion")
        self.labelVersion.setText("asdasd")
        self.pushLogin = QtWidgets.QPushButton(self.centralwidget)
        self.pushLogin.setGeometry(QtCore.QRect(210, 500, 90, 32))
        self.pushLogin.setFlat(False)
        self.pushLogin.setObjectName("pushLogin")
        self.pushLogin.clicked.connect(self.load_dashboard)
        LoginWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(LoginWindow)
        self.statusbar.setObjectName("statusbar")
        LoginWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Offstack Login"))
        self.lineEmailInput.setPlaceholderText(_translate("LoginWindow", "Email"))
        self.linePasswordInput.setPlaceholderText(_translate("LoginWindow", "Password"))
        self.labelTitle.setText(_translate("LoginWindow", "Offstack"))
        self.labelVersion.setText(_translate("LoginWindow", "v{}".format(VERSION)))
        self.pushLogin.setText(_translate("LoginWindow", "Login"))


# if __name__ == "__main__":
#     import sys
    # app = QtWidgets.QApplication(sys.argv)
    # LoginWindow = QtWidgets.QMainWindow()
    # ui = LoginWindow()
    # ui.setupUi(LoginWindow)
    # LoginWindow.show()
    # # sys.exit(app.exec_())
