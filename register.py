from PyQt5 import QtCore, QtGui, QtWidgets
from chat import ChatApp
from login import LoginApp
from database import Database

class Ui_RegisterWindow(object):
    def setupUi(self, RegisterWindow):
        RegisterWindow.setObjectName("RegisterWindow")
        RegisterWindow.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(RegisterWindow)
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
        self.confirm_password_input = QtWidgets.QLineEdit(self.centralwidget)
        self.confirm_password_input.setGeometry(QtCore.QRect(80, 150, 240, 30))
        self.confirm_password_input.setObjectName("confirm_password_input")
        self.confirm_password_input.setPlaceholderText("Confirm password")
        self.confirm_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.register_button = QtWidgets.QPushButton(self.centralwidget)
        self.register_button.setGeometry(QtCore.QRect(160, 200, 80, 30))
        self.register_button.setObjectName("register_button")
        self.register_button.setText("Register")
        self.already_have_account_link = QtWidgets.QLabel('Đã có tài khoản?', self.centralwidget)
        self.already_have_account_link.setGeometry(QtCore.QRect(160, 240, 150, 20))
        self.already_have_account_link.setObjectName("already_have_account_link")
        self.already_have_account_link.setText('<a href="#">Đã có tài khoản?</a>')
        self.already_have_account_link.linkActivated.connect(self.open_login_window)
        RegisterWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(RegisterWindow)
        QtCore.QMetaObject.connectSlotsByName(RegisterWindow)

    def retranslateUi(self, RegisterWindow):
        _translate = QtCore.QCoreApplication.translate
        RegisterWindow.setWindowTitle(_translate("RegisterWindow", "Đăng ký tài khoản"))

# Additional code for interaction and functionality
class RegisterApp(QtWidgets.QMainWindow, Ui_RegisterWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.register_button.clicked.connect(self.register_user)
        self.confirm_password_input.returnPressed.connect(self.register_user)
        self.db = Database('users.db')  # Connect to the database

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not password or not confirm_password:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Please enter all information.')
            return
        
        if password != confirm_password:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Passwords do not match.')
            return

        # Insert user into the database
        self.db.insert_user(username, password)

        print("Registered User:")
        print("Username:", username)
        print("Password:", password)

        self.show_login_window()  # Show login window after successful registration

    def show_login_window(self):
        self.login_window = LoginApp()
        self.login_window.show()
        self.close()

    def open_login_window(self):
        self.login_window = LoginApp()
        self.login_window.show()
        self.close()