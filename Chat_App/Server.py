from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM

address = ("192.168.1.30", 8000)
addresses = {}
names = {}


def get_command(server_sock):  # main thread
    Thread(target=accept_incoming_connections, args=(server_sock,), daemon=True).start()
    while True:
        command = input()
        if command == "shutdown()":
            print("Server is closing...")
            for sock in addresses:
                sock.close()
            server_sock.close()
            break
        """ if command == bla bla """


def accept_incoming_connections(server_sock):   # sürekli bağlantı var mı kontrol eden thread
    while True:
        client_sock, addr = server_sock.accept()
        Thread(target=handle_incoming_request, args=(client_sock, addr), daemon=True).start()


def handle_incoming_request(client_sock, addr):   # gelen bağlantıyı kabul eden thread(sonsuz döngü yok)
    try:
        addresses[client_sock] = addr
        print("{} : {} has connected to the server.".format(addr[0], addr[1]))
        name = client_sock.recv(1024)
        names[client_sock] = name
        broadcast(client_sock, name + " has entered the room.".encode())
        Thread(target=handle_client, args=(client_sock,), daemon=True).start()
    except ConnectionResetError:
        print("{} : {} has disconnected.".format(addresses[client_sock][0], addresses[client_sock][1]))
        del addresses[client_sock]   # ismi alırken sıkıntı çıktığı için ismi silmiyoruz
        client_sock.close()


def handle_client(client_sock):    # istemci threadi
    while True:
        try:
            data = client_sock.recv(1024)
            prefix = names[client_sock]+": ".encode()
            broadcast(client_sock, data, prefix=prefix)
        except ConnectionResetError:
            print("{} : {} has disconnected.".format(addresses[client_sock][0], addresses[client_sock][1]))
            del addresses[client_sock], names[client_sock]
            break


def broadcast(client_sock, data, prefix=None):
    try:
        for sock in names.keys():
            if sock == client_sock:
                continue
            elif not prefix:
                sock.send(data)
            else:
                sock.send(prefix + data)
    except ConnectionAbortedError:
        pass


if __name__ == "__main__":
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(address)
    print("Server has started. ({} : {})\n".format(address[0], address[1]))
    server_socket.listen(4)
    get_command(server_socket)  # main thread
