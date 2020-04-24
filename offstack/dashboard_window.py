from PyQt5 import QtCore, QtGui, QtWidgets
from offstack.managers import oAuthManager, DriverManager
from requests_oauthlib import OAuth2Session

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

opts = Options()
opts.headless = True
opts.add_argument('--no-sandbox')

assert opts.headless  # Operating in headless mode

from offstack.dialog import App
from offstack.logger import logger

from offstack.utils import (
    check_access_token,
    request_access_token,
    get_user_credentials,
    request_favorites,
    get_questions,
    display_favorite
)

from offstack.constants import(
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI,
    SCOPE,
    USERDATA
)

class DashboardWindow(QtWidgets.QMainWindow):

    def cache_favorites(self):
        logger.debug("Creating oAuth Session")
        oauth_manager = oAuthManager(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, OAuth2Session, SCOPE)
        oauth_manager.create_session()
        if not check_access_token():
            browser = Firefox(options=opts)

            driver = DriverManager(CLIENT_ID, CLIENT_SECRET, browser)

            user_data = get_user_credentials()

            resp = request_access_token(driver, oauth_manager, user_data)
            if not resp:
                App().initUI("information", "Offstack Dialog", "Unable to get the access token.")
                return
        
        if request_favorites(oauth_manager):
            # self.populate_on_load(response_list=display_favorites())
            return get_questions()
        else:
            return False
    
    def populate_on_load(self):
        response_list = get_questions()

        if not response_list:
            print("No questions need to cache")
            response_list = self.cache_favorites()
        
        if response_list:
            for row in response_list:
                item = QtWidgets.QListWidgetItem()
                item.setData(0, row["title"])
                item.setData(0x0100, row["question_id"])
                self.listQuestions.addItem(item)

    def selected_row(self, qmodelindex):
        item = self.listQuestions.currentItem()
        resp = display_favorite(qmodelindex.data(0x0100))
        if resp:
            self.plainTextEditContent.clear()
            self.plainTextEditContent.setReadOnly(True)
            self.plainTextEditContent.appendHtml(resp)
            # self.plainTextEditContent.setPosition(0)
            # self.plainTextEditContent.insertPlainText(resp)
        

    def setupUi(self, DashboardWindow):
        DashboardWindow.setObjectName("DashboardWindow")
        DashboardWindow.resize(873, 623)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DashboardWindow.sizePolicy().hasHeightForWidth())
        DashboardWindow.setSizePolicy(sizePolicy)
        DashboardWindow.setMaximumSize(QtCore.QSize(1920, 1080))
        DashboardWindow.setDockOptions(QtWidgets.QMainWindow.AllowNestedDocks|QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(DashboardWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(15, 20, 15, 0)
        self.gridLayout.setSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.lineSearchInQuestions = QtWidgets.QLineEdit(self.centralwidget)
        self.lineSearchInQuestions.setInputMethodHints(QtCore.Qt.ImhPreferLowercase)
        self.lineSearchInQuestions.setObjectName("lineSearchInQuestions")
        self.gridLayout.addWidget(self.lineSearchInQuestions, 0, 0, 1, 1)
        self.plainTextEditContent = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.plainTextEditContent.sizePolicy().hasHeightForWidth())
        self.plainTextEditContent.setSizePolicy(sizePolicy)
        self.plainTextEditContent.setObjectName("plainTextEditContent")
        self.gridLayout.addWidget(self.plainTextEditContent, 0, 1, 2, 1)
        # self.listQuestions = QtWidgets.QListView(self.centralwidget)
        self.listQuestions = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listQuestions.sizePolicy().hasHeightForWidth())
        self.listQuestions.setSizePolicy(sizePolicy)
        self.listQuestions.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.listQuestions.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.listQuestions.setObjectName("listQuestions")
        self.gridLayout.addWidget(self.listQuestions, 1, 0, 1, 1)
        self.listQuestions.clicked.connect(self.selected_row)
        # (widget, int fromRow, int fromColumn, int rowSpan, int columnSpan, Qt::Alignment alignment = 0)
        DashboardWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DashboardWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 873, 28))
        self.menubar.setObjectName("menubar")
        self.menuMore = QtWidgets.QMenu(self.menubar)
        self.menuMore.setObjectName("menuMore")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        DashboardWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DashboardWindow)
        self.statusbar.setObjectName("statusbar")
        DashboardWindow.setStatusBar(self.statusbar)
        self.actionConfigurations = QtWidgets.QAction(DashboardWindow)
        self.actionConfigurations.setMenuRole(QtWidgets.QAction.PreferencesRole)
        self.actionConfigurations.setObjectName("actionConfigurations")
        self.actionQuit = QtWidgets.QAction(DashboardWindow)
        self.actionQuit.setMenuRole(QtWidgets.QAction.QuitRole)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtWidgets.QAction(DashboardWindow)
        self.actionAbout.setMenuRole(QtWidgets.QAction.AboutRole)
        self.actionAbout.setObjectName("actionAbout")
        self.actionCacheFavorites = QtWidgets.QAction(DashboardWindow)
        self.actionCacheFavorites.setObjectName("actionCacheFavorites")
        self.actionCacheFavorites.triggered.connect(self.cache_favorites)
        self.menuMore.addAction(self.actionCacheFavorites)
        self.menuMore.addSeparator()
        self.menuMore.addAction(self.actionConfigurations)
        self.menuMore.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuMore.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(DashboardWindow)
        QtCore.QMetaObject.connectSlotsByName(DashboardWindow)
        
        self.populate_on_load()

    def retranslateUi(self, DashboardWindow):
        _translate = QtCore.QCoreApplication.translate
        DashboardWindow.setWindowTitle(_translate("DashboardWindow", "Offstack Dashboard"))
        self.lineSearchInQuestions.setPlaceholderText(_translate("DashboardWindow", "Search for questions or keywords..."))
        self.plainTextEditContent.setPlainText(_translate("DashboardWindow", "Detailed information about each question"))
        self.menuMore.setTitle(_translate("DashboardWindow", "More"))
        self.menuHelp.setTitle(_translate("DashboardWindow", "Help"))
        self.actionConfigurations.setText(_translate("DashboardWindow", "Configurations"))
        self.actionQuit.setText(_translate("DashboardWindow", "Quit"))
        self.actionAbout.setText(_translate("DashboardWindow", "About"))
        self.actionCacheFavorites.setText(_translate("DashboardWindow", "Cache Favorites"))


# if __name__ == "__main__":
#     import sys
#     # app = QtWidgets.QApplication(sys.argv)
#     DashboardWindow = QtWidgets.QMainWindow()
#     ui = DashboardWindow()
#     ui.setupUi(DashboardWindow)
#     DashboardWindow.show()
#     # sys.exit(app.exec_())
