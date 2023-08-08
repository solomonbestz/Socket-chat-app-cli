import socket
import threading


def listen_for_messages(client: object, username: str) -> None:
    while True:
        msg = client.recv(2048).decode('utf-8')

        if msg:
            final_msg = f'@{username}:{msg}'
            send_message(final_msg)
        else:
            print(f'Empty Message From {username}')

def send_message_to_user(client: object, message: str) -> None:
    client.sendall(message.encode())

def send_message(message: str) -> None:
    for user in active_users:
        send_message_to_user(user[1], message)
        

def connections_handler(client: object) -> None:
    
    #get client message that contains user_name
    while 1:
        username = client.recv(2048).decode('utf-8')

        if username:
            active_users.append((username, client))
            break
        else:
            print('Client Username is empty')

    threading.Thread(target=listen_for_messages, args=(client, username,)).start()

def main() -> None:
    # Instantiating the socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f'Running the server on {HOST} {PORT}')
    except:
        print(f'Unable To Bind To Host {HOST} and Port {PORT}')

    # Server Limit
    server.listen(SERVER_LIMIT)
    print(f'{server.__class__.__name__} is listening for connection')

    while 1:
        client, address = server.accept()
        print(f'Successfully connected to client {address[0]} {address[1]}')

        threading.Thread(target=connections_handler, args=(client, )).start()
    


if __name__=='__main__':
    HOST = '127.0.0.1'
    PORT = 1234
    SERVER_LIMIT = 5
    active_users = []
    main()
