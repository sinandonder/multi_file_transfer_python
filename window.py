import sys
from _thread import start_new_thread
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QGroupBox, QFormLayout,
    QPushButton, QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QWidget, QStatusBar, QInputDialog, QFileDialog
)

from PyQt5.QtGui import QFont


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.function_name = ''
        self.vertical_layout = QVBoxLayout()
        self.horizontal_layout = QHBoxLayout()
        self.label_ip = QLabel("IP:")
        self.label_port = QLabel("PORT:")
        self.line_ip = QLineEdit()
        self.line_port = QLineEdit()
        self.button_start = QPushButton("Start")
        self.label_connected_users = QLabel("0 User(s) Online")
        self.list_users = QListWidget()
        self.status_bar = QStatusBar()
        self.style = open("style.css", 'r').read()
        self.setStyleSheet(self.style)
        self.input_dialog = QInputDialog()

        self.horizontal_layout.addWidget(self.label_ip)
        self.horizontal_layout.addWidget(self.line_ip)
        self.horizontal_layout.addWidget(self.label_port)
        self.horizontal_layout.addWidget(self.line_port)

        self.setLayout(self.vertical_layout)
        self.vertical_layout.addLayout(self.horizontal_layout)
        self.vertical_layout.addWidget(self.button_start)
        self.vertical_layout.addWidget(self.label_connected_users)
        self.vertical_layout.addWidget(self.list_users)
        self.vertical_layout.addWidget(self.status_bar)

        #lambda: self.updateTextBox(self.getExtText())

        self.button_start.clicked.connect(self.start_event)
        self.status_bar.showMessage("NOT CONNECTED.")

        self.list_users.setSpacing(5)
        self.list_users.itemClicked.connect(self.item_clicked)
        #self.list_users.setItemAlignment()
    def start_event(self):
        self.button_start.setText("Stop")
        self.button_start.clicked.connect(self.stop_event)
        start_new_thread(self.function_name, tuple())
        

    def stop_event(self):
        self.button_start.setText("Start")
        self.button_start.clicked.connect(self.start_event)
        start_new_thread(self.function_name, tuple())

    def update_list_users(self, user_list):
        self.list_users.clear()
        for username in user_list:
            #QListWidgetItem(username, self.list_users).setToolTip(f"Send File to {username}")
            item = QListWidgetItem(username)
            item.setToolTip(f"Send File to {username}")
            serifFont = QFont("SansSerif", 13)
            item.setFont(serifFont)
            self.list_users.addItem(item)

            """
            item = QListWidgetItem()
            item_widget = QWidget()

            line_text_username = QLabel(username)
            line_button_send = QPushButton("Send")
            line_button_send.setObjectName(str(username))
            line_button_send.clicked.connect(self.clicked)

            item_layout = QHBoxLayout()
            item_layout.addWidget(line_text_username)
            item_layout.addWidget(line_button_send)

            item_widget.setLayout(item_layout)
            item.setSizeHint(item_widget.sizeHint())

            self.list_users.addItem(item)
            self.list_users.setItemWidget(item, item_widget)
            """

        self.label_connected_users.setText(f"{len(user_list)} User(s) Online")

    def clicked(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        print(f'click: {push_button.objectName()}')
    
    def item_clicked(self):
        file , check = QFileDialog.getOpenFileName(None, "Select a File",
                                               "", "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
        if check:
            print(file)



        #start_new_thread(print, (item.text(), ))
    
    def show_username_dialog(self):
        username, ok = self.input_dialog.getText(self, "Username", "Username: ")
        if ok:
            return username
        else:
            return 'user1'


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.setWindowTitle("Server")
    window.update_list_users(['sinan', 'john', 'Jeremy'])
    window.show()
    sys.exit(app.exec_())
