import asyncio
from my_classes import Server


SERVER_IP = "127.0.0.1"
SERVER_PORT = 65432

if __name__ == "__main__":
    as_loop = asyncio.get_event_loop()
    server_main = Server(SERVER_IP, SERVER_PORT, as_loop)
    server_main.run_server()
