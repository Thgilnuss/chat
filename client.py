import socket
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 1024

def receive_messages(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f'Received data: {data.decode("utf-8")}')
    except ConnectionResetError:
        print('Disconnected from the server.')
    finally:
        client_socket.close()



def start_client():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_HOST, SERVER_PORT))
        print(f'Connected to server at {SERVER_HOST}:{SERVER_PORT}')

        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.start()

        try:
            while True:
                message = input("Enter message: ")
                client.sendall(message.encode('utf-8'))
        except KeyboardInterrupt:
            print("Client is closing.")
        finally:
            client.close()
    except ConnectionRefusedError:
        print("Could not connect to the server. Make sure the server is running.")

def send_message_to_server(message):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_HOST, SERVER_PORT))
        client.sendall(message.encode('utf-8'))
        client.close()
    except ConnectionRefusedError:
        print("Could not connect to the server. Make sure the server is running.")


if __name__ == '__main__':
    start_client()
