import socket
import threading


def listen_for_servers_messages(client):
    while 1:
        message = client.recv(2048).decode('utf-8') 
        if message:
            user_name = message.split(':')[0]
            content = message.split(':')[1]

            print(f'[{user_name}] {content}')
        else:
            print('message recieved from client is empty')

def send_message_to_server(client):
    while 1:
        message = input('Message: ')
        if message:
            client.sendall(message.encode())
        else:
            print('Empty Message')
            exit(0)


def communicate_with_server(client):
    user_name = input('Enter Username: ')
    if user_name:
        client.sendall(user_name.encode())
    else:
        print('Username cannot be empty')
        exit(0)

    threading.Thread(target=listen_for_servers_messages, args=(client,)).start()
    send_message_to_server(client)
    

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print('Successfully Connected...')
    except Exception:
        print('Unable To Connect To Server')

    communicate_with_server(client)


if __name__=='__main__':
    HOST = '127.0.0.1'
    PORT = 1234
    main()