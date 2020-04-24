import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Offstack'
        self.left = 10
        self.top = 100
        self.width = 500
        self.height = 500
        
    def initUI(self, type, dialog_header, header_message):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # buttonReply = QMessageBox.information(self, dialog_header, header_message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if type == "noicon":
            buttonReply = QMessageBox.noicon(self, dialog_header, header_message, QMessageBox.Ok)
            return_response = True if buttonReply == QMessageBox.Ok else False
        elif type == "question":
            buttonReply = QMessageBox.question(self, dialog_header, header_message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            return_response = True if buttonReply == QMessageBox.Yes else False
        elif type == "information":
            buttonReply = QMessageBox.information(self, dialog_header, header_message, QMessageBox.Ok)
            return_response = True if buttonReply == QMessageBox.Ok else False
        elif type == "Warning":
            buttonReply = QMessageBox.warning(self, dialog_header, header_message, QMessageBox.Ok | QMessageBox.Cancel , QMessageBox.Cancel)
            return_response = True if buttonReply == QMessageBox.Ok else False
        elif type == "critical":
            buttonReply = QMessageBox.critical(self, dialog_header, header_message, QMessageBox.Ok | QMessageBox.Abort , QMessageBox.Abort)
            return_response = True if buttonReply == QMessageBox.Ok else False

        # if buttonReply == QMessageBox.Yes:
        #     return True
        # else:
        #     return False
        return return_response
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_()) 