import socket
import threading


def get_message(conn, addr):
    while True:
        data = conn.recv(1024)
        print(f"from {addr[1]} -> {data.decode()}")
        if not data:
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
    conn, addr = s.accept()
    print(f"Connected by {addr[1]}")

    threading.Lock().acquire()
    thread_get_message = threading.Thread(target=get_message, args=(conn, addr))
    thread_get_message.start()

s.close()
