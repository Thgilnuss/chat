import sys
import threading
from PyQt5 import QtWidgets
from register import RegisterApp
from server import start_server
from client import start_client

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    register_window = RegisterApp()
    register_window.show()
    register_window.already_have_account_link.linkActivated.connect(register_window.open_login_window)

    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    client_thread = threading.Thread(target=start_client)
    client_thread.start()

    sys.exit(app.exec_())
