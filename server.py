import socket
import asyncio

SERVER_IP = ""  # Standard loopback interface address (localhost)
SERVER_PORT = 65432  # Port to listen on (non-privileged ports are > 1023)




if __name__ == "__main__":
    as_loop = asyncio.get_event_loop()
    server_main = Server(SERVER_IP, SERVER_PORT, as_loop)
    server_main.run_server()
