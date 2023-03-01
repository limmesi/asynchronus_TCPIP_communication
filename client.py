import asyncio
from my_classes import Client

SERVER_IP = "127.0.0.1"
SERVER_PORT = 65432

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    client = Client(SERVER_IP, SERVER_PORT, loop)
    asyncio.run(client.connect_to_server())
