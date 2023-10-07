import socket
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 1024

clients = []
clients_lock = threading.Lock()

def broadcast(message):
    with clients_lock:
        for client_socket in clients:
            try:
                client_socket.sendall(message)
            except:
                clients.remove(client_socket)

def handle_client(client_socket):
    try:
        with clients_lock:
            clients.append(client_socket)

        print(f'Client connected: {client_socket.getpeername()}')

        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            print(f'Received from {client_socket.getpeername()}: {data.decode("utf-8")}')

            broadcast(data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print(f'Client disconnected: {client_socket.getpeername()}')
        with clients_lock:
            clients.remove(client_socket)
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)

    print(f'Server is listening on {SERVER_HOST}:{SERVER_PORT}')

    try:
        while True:

            client_socket, client_addr = server.accept()
            print(f'Accepted connection from {client_addr}')

            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:

        with clients_lock:
            for client_socket in clients:
                client_socket.close()
        server.close()

if __name__ == '__main__':
    start_server()
