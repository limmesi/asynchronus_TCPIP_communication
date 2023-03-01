import asyncio
from my_classes import Client


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    client = Client("127.0.0.1", 65432, loop)
    asyncio.run(client.connect_to_server())
