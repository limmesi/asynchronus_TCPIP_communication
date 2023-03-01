import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))
print(f"Connected by {HOST}:{PORT}")
# data = s.recv(1024)
# print(f"Received: {data!r}")
while True:
    message = input("me: ")
    if message == '/quit':
        break
    s.sendall(message.encode())
    data = s.recv(1024)
    print("somebody: ", data.decode())

s.close()
