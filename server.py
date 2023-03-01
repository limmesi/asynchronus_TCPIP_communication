import asyncio
from my_classes import Server


if __name__ == "__main__":
    as_loop = asyncio.new_event_loop()
    server_main = Server("127.0.0.1", 65432, as_loop)
    server_main.run_server()
