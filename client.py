import socket
import pickle
import sys


from package import Package
from PyQt5.QtWidgets import QApplication
from window import Window


SERVER_ADDR = socket.gethostbyname(socket.gethostname())
PORT = 6000
ADDR = (SERVER_ADDR, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def start_client():

    try:
        client.connect(ADDR) 
        print("[CONNECTED] Connected to Server.")
    except socket.error as error:
        print(error)
        return
    
    window.status_bar.showMessage(f"[CONNECTED] IP {SERVER_ADDR} PORT: {PORT}")
    window.setWindowTitle(f"CLIENT: {username}")

    start = True
    
    package = get_package()

    while start:
        if package.message == "username":
            #username = input("Username: ")
            #username = window.show_username_dialog()
            client.send(pickle.dumps(username))

        elif package.message == "user_list":
            user_list = list(package.file)
            user_list.remove(username)
            window.update_list_users(user_list)

        elif package.message == "file":
            print(package.file)

        package = get_package()

        """
        if username == "sinan":
            send_package("user", "file")
        """
        

def get_user_list():
    while True:
        try:
            user_list = pickle.loads(client.recv(4096))
            print(user_list)
        except socket.error as error:
            print(error)
        

def send_package(username, file):
    package = Package(username, file)

    try:
        client.send(pickle.dumps(package))
        return pickle.loads(client.recv(4096))
    except socket.error as error:
        print(error)

def get_package():
    try:
        return pickle.loads(client.recv(4096))
    except socket.error as error:
        print("test", error)




if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Window()
    window.setWindowTitle("Client")
    window.function_name = start_client
    window.line_ip.setText(socket.gethostbyname(socket.gethostname()))
    window.line_port.setText("6000")
    

    window.show()
    username = window.show_username_dialog()
    sys.exit(app.exec_())