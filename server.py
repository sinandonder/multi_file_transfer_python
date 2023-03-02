import socket
import pickle
import sys

from _thread import start_new_thread
from package import Package
from window import Window
from PyQt5.QtWidgets import QApplication


users_dict = {}


def start():
    window.function_name = stop

    try:
        SERVER_ADDR = window.line_ip.text()
        PORT = int(window.line_port.text())
        global server 
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind((SERVER_ADDR, PORT))
        server.listen()
    except socket.error as e:
        window.status_bar.showMessage(str(e))
        return
    except ValueError as e:
        window.status_bar.showMessage("Ip and Port values are not valid!")
        return
    
    start = True

    window.status_bar.showMessage(f"[INFO] Server started. IP {SERVER_ADDR} PORT: {PORT}")
    window.setWindowTitle(f"SERVER - {SERVER_ADDR}:{PORT}")


    while start:
        try:
            conn, addr = server.accept()
        except socket.error as error:
            window.status_bar.showMessage(str(error))
            server.close()
            return
        
        start_new_thread(handle_client, (conn, ))

def stop():
    window.function_name = start
    server.close()

def send(conn, package):
    try:
        conn.send(pickle.dumps(package))
        return pickle.loads(conn.recv(4096))
    except socket.error as error:
        print(error)


def send_package(package):
    user, package.message = package.message, "file"
    
    try:
        conn = users_dict[user]
        conn.send(pickle.dumps(package))
    except socket.error as error:
        print(error)
    except KeyError as error:
        print(f"[ERROR] Check User Name!{error}")

def get_package(conn):
    try:
        username = conn.recv(1024)
        line = conn.recv(1024)
        file = ''

        while line:
            file += line
            line = conn.recv(1024)

        return Package(username, file)
    except socket.error as error:
        print(error)


def send_user_list(package):
    try:
        for conn in users_dict.values():
            conn.sendall(pickle.dumps(package))
    except socket.error as error:
        print(error)


def handle_client(conn):
    package = Package("username")
    username = send(conn, package)
        
    while username in users_dict.keys():
        username = send(conn, package)
        
    users_dict[username] = conn
    print(users_dict.keys())

    window.update_list_users(users_dict.keys())
    

    package = Package("user_list", list(users_dict.keys()))
    send_user_list(package)

    start = True

    while start:
        try:
            package = get_package(conn)
            send_package(package)
        except socket.error as error:
            conn.close()
            users_dict.pop(username)
            window.update_list_users(users_dict.keys())
            start = False
        


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Window()
    window.setWindowTitle("Server")
    window.function_name = start
    window.line_ip.setText(socket.gethostbyname(socket.gethostname()))
    window.line_port.setText("6000")
    window.show()

    sys.exit(app.exec_())


    

