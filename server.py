import socket
import threading


def get_message():
    conn, addr = s.accept()
    print(f"Connected by {addr[1]}")
    while True:
        with open("my_file.txt", "r") as f:
            data_to_send = f.readlines()[-1]
        if data_to_send.split()[0] == addr[1]:
            to_send = data_to_send.split()[1:]
            conn.sendall(to_send.encode())
        else:
            conn.sendall(b'')
        data_received = conn.recv(1024)
        print(f"from {addr[1]} -> {data_received.decode()}")
        with open("my_file.txt", "a") as f:
            f.write(f"{addr[1]} {data_received.decode()}\n")
        if not data_received:
            break
    conn.close()


def send_message():
    pass


HOST = ""  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
i = 0
while True:
    threading.Lock().acquire()
    thread_get_message = threading.Thread(target=get_message)
    thread_get_message.start()
    if not threading.active_count():
        break

s.close()
