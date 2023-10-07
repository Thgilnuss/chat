from PyQt5 import QtWidgets, QtGui, QtCore
from client import send_message_to_server
import pymysql


MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '1234'
MYSQL_DB = 'chat_app'

def connect_to_mysql():
    return pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB)

def save_message_to_mysql(sender, content):
    connection = connect_to_mysql()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO messages (sender, content) VALUES (%s, %s)"
            cursor.execute(sql, (sender, content))
            connection.commit()
    finally:
        connection.close()

class EmojiDialog(QtWidgets.QWidget):
    emoji_clicked = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.Popup)
        self.emojis =["😊", "😂", "😍", "👍", "🎉", "😎", "😘", "🤗", "😇", "😉",
                    "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇"]
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QGridLayout()
        for i, emoji in enumerate(self.emojis):
            button = QtWidgets.QPushButton(emoji, self)
            button.clicked.connect(lambda _, e=emoji: self.emoji_clicked.emit(e))
            button.setStyleSheet("font-size: 20px; padding: 5px; border: none; border-radius: 10px;")
            layout.addWidget(button, i // 5, i % 5)

        layout.setContentsMargins(10, 10, 10, 10)
        layout.setVerticalSpacing(10)
        layout.setHorizontalSpacing(10)

        container = QtWidgets.QWidget()
        container.setLayout(layout)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(container)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.chat_display = QtWidgets.QTextEdit(self.centralwidget)
        self.chat_display.setObjectName("chat_display")
        self.verticalLayout.addWidget(self.chat_display)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.message_input = QtWidgets.QLineEdit(self.centralwidget)
        self.message_input.setObjectName("message_input")
        self.message_input.setPlaceholderText("Nhập tin nhắn ...")
        self.horizontalLayout.addWidget(self.message_input)

        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_button.setObjectName("send_button")
        self.send_button.setText("Gửi")
        self.horizontalLayout.addWidget(self.send_button)

        self.emoji_button = QtWidgets.QPushButton(self.centralwidget)
        self.emoji_button.setObjectName("emoji_button")
        self.emoji_button.setText("😊")
        self.horizontalLayout.addWidget(self.emoji_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.emoji_dialog = EmojiDialog(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chat App"))

class ChatApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, username):
        super().__init__()
        self.setupUi(self)
        self.username = username
        self.setWindowTitle(f"Chat App - {self.username}")
        self.send_button.clicked.connect(self.send_message)
        self.message_input.returnPressed.connect(self.send_message)
        self.chat_display.setReadOnly(True)
        self.message_input.setFocus()
        self.selected_emojis = []

        self.emoji_dialog.emoji_clicked.connect(self.insert_emoji)

        self.emoji_button.clicked.connect(self.show_emoji_dialog)

        self.setStyleSheet("""
            background-color: #f0f0f0;
        """)
        self.chat_display.setStyleSheet("""
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #d8d8d8;
            border-radius: 10px;
            padding: 10px;
            font-family: Arial, sans-serif;
            font-size: 14px;
        """)
        self.message_input.setStyleSheet("""
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #d8d8d8;
            border-radius: 20px;
            padding: 10px;
            font-family: Arial, sans-serif;
            font-size: 14px;
        """)
        self.send_button.setStyleSheet("""
            background-color: #0084ff;
            color: #ffffff;
            border: 1px solid #0084ff;
            border-radius: 20px;
            padding: 10px 20px;
            font-family: Arial, sans-serif;
            font-size: 14px;
        """)
        self.emoji_button.setStyleSheet("""
            font-size: 20px;
            padding: 5px;
            border: none;
        """)


    def show_emoji_dialog(self):
        button_pos = self.emoji_button.mapToGlobal(QtCore.QPoint(0, 0))
        dialog_x = button_pos.x()
        dialog_y = button_pos.y() - self.emoji_dialog.height()

        self.emoji_dialog.move(dialog_x, dialog_y)
        self.emoji_dialog.show()

    def insert_emoji(self, emoji):
        self.selected_emojis.append(emoji)
        current_text = self.message_input.text()
        cursor_position = self.message_input.cursorPosition()
        new_text = current_text[:cursor_position] + emoji + current_text[cursor_position:]
        self.message_input.setText(new_text)
        self.message_input.setCursorPosition(cursor_position + len(emoji))
        

    def send_message(self):
        message = self.message_input.text().strip()
        
        if message:
            message_with_emoji = ""
            send_message_to_server(message)

            for emoji in self.selected_emojis:
                emoji_with_style = f'<span style="font-size: 20px;">{emoji}</span>'
                message = message.replace(emoji, emoji_with_style)

            message_with_emoji += message

            formatted_message = f"<b>{self.username}:</b> {message}<br>"
            self.chat_display.append(formatted_message)
            save_message_to_mysql(self.username, message)
            self.selected_emojis = []
        self.message_input.clear()
        