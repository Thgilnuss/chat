from PyQt5 import QtCore, QtGui, QtWidgets
from chat import ChatApp
from database import Database

class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.username_input = QtWidgets.QLineEdit(self.centralwidget)
        self.username_input.setGeometry(QtCore.QRect(80, 50, 240, 30))
        self.username_input.setObjectName("username_input")
        self.username_input.setPlaceholderText("Enter username")
        self.password_input = QtWidgets.QLineEdit(self.centralwidget)
        self.password_input.setGeometry(QtCore.QRect(80, 100, 240, 30))
        self.password_input.setObjectName("password_input")
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_button = QtWidgets.QPushButton(self.centralwidget)
        self.login_button.setGeometry(QtCore.QRect(160, 150, 80, 30))
        self.login_button.setObjectName("login_button")
        self.login_button.setText("Login")
        
        LoginWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Đăng nhập"))

# Additional code for interaction and functionality
class LoginApp(QtWidgets.QMainWindow, Ui_LoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.login_button.clicked.connect(self.login)
        self.db = Database('users.db')  # Connect to the database
        self.password_input.returnPressed.connect(self.login)
        self.username_input.returnPressed.connect(self.login)



    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Please enter all information.')
            return

        # Get user from the database
        user = self.db.get_user(username)

        if user and user[2] == password:
            print("Login User:")
            print("Username:", username)
            print("Password:", password)

            self.show_chat_window(username)  # Show chat window after successful login
        else:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Invalid username or password.')

    def show_chat_window(self, username):
        self.chat_window = ChatApp(username)
        self.chat_window.show()
        self.close()