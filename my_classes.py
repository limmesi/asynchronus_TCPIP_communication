import asyncio
from aioconsole import ainput


class ClientOnServer:
    last_id = 1

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer
        self.ip = writer.get_extra_info('peername')[0]
        self.port = writer.get_extra_info('peername')[1]
        self.id = ClientOnServer.last_id
        ClientOnServer.last_id += 1

    async def get_message(self):
        message = await self.reader.read(255)
        return str(message.decode('utf8'))


class Server:
    def __init__(self, server_ip: str, server_port: int, loop: asyncio.AbstractEventLoop):
        self.server_ip = server_ip
        self.server_port = server_port
        self.loop = loop
        self.clients: dict[asyncio.Task, ClientOnServer] = {}

    def run_server(self):
        try:
            server = asyncio.start_server(self.accept_client, self.server_ip, self.server_port)
            self.loop.run_until_complete(server)
            self.loop.run_forever()
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("Keyboard Interrupt Detected. Shutting down!")

        self.shutdown_server()

    def accept_client(self, client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter):
        client = ClientOnServer(client_reader, client_writer)
        task = asyncio.Task(self.incoming_client_message_callback(client))
        self.clients[task] = client

        client_ip = client_writer.get_extra_info('peername')[0]
        client_port = client_writer.get_extra_info('peername')[1]
        print(f"New Connection: {client_ip}:{client_port}")

        task.add_done_callback(self.disconnect_client)

    async def incoming_client_message_callback(self, client: ClientOnServer):
        while True:
            client_message = await client.get_message()
            if client_message.startswith("quit"):
                break
            else:
                self.broadcast(f"{client.id}: {client_message}".encode('utf8'))
            await client.writer.drain()

        print(f"Client {client.id} Disconnected!")

    def broadcast(self, message: bytes):
        for client in self.clients.values():
            client.writer.write(message)

    def disconnect_client(self, task: asyncio.Task):
        client = self.clients[task]

        self.broadcast(f"{client.id} has left!".encode('utf8'))

        del self.clients[task]
        client.writer.write('quit'.encode('utf8'))
        client.writer.close()
        print("End Connection")

    def shutdown_server(self):
        print("Shutting down server!")
        for client in self.clients.values():
            client.writer.write('quit'.encode('utf8'))
        self.loop.stop()


class Client:
    def __init__(self, server_ip: str, server_port: int, loop: asyncio.AbstractEventLoop):
        self.server_ip: str = server_ip
        self.server_port: int = server_port
        self.loop: asyncio.AbstractEventLoop = loop
        self.reader = None
        self.writer = None

    async def connect_to_server(self):
        try:
            self.reader, self.writer = await asyncio.open_connection(self.server_ip, self.server_port)
            await asyncio.gather(self.receive_messages(), self.start_client_cli())
        except Exception as e:
            print(e)
        print("Shutting down")

    async def receive_messages(self):
        server_message = ''
        while server_message != 'quit':
            server_message = await self.get_server_message()
            print(f"{server_message}")
        # if self.loop.is_running():
        self.loop.stop()

    async def get_server_message(self):
        server_message = await self.reader.read(255)
        return str(server_message.decode('utf8'))

    async def start_client_cli(self):
        client_message = ''
        while client_message != 'quit':
            client_message = await ainput("")
            self.writer.write(client_message.encode('utf8'))
            await self.writer.drain()

        # self.loop.is_running():
        self.loop.stop()



