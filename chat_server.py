import socket
import threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = None

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        self.clients.append(client_socket)

        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                self.broadcast(message, client_socket)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            self.clients.remove(client_socket)
            client_socket.close()

    def broadcast(self, message, client_socket):
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    client.close()
                    self.clients.remove(client)

if __name__ == "__main__":
    server = ChatServer('localhost', 8888)
    server.start()
