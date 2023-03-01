import asyncio

class Client:
    last_id = 1
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer
        self.ip = writer.get_extra_info('peername')[0]
        self.port = writer.get_extra_info('peername')[1]
        self.id = Client.last_id
        Client.last_id += 1

class Server:
    def __init__(self, server_ip: str, server_port: int, loop: asyncio.AbstractEventLoop):
        self.server_ip = server_ip
        self.server_port = server_port
        self.loop = loop
        self.clients: dict[asyncio.Task, Client] = {}

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
        client = Client(client_reader, client_writer)
        task = asyncio.Task(self.incoming_client_message_cb(client))
        self.clients[task] = client

        client_ip = client_writer.get_extra_info('peername')[0]
        client_port = client_writer.get_extra_info('peername')[1]
        print(f"New Connection: {client_ip}:{client_port}")

        task.add_done_callback(self.disconnect_client)


    async def incoming_client_message_callback(self):
        pass

    def broadcast(self):
        pass

    def disconnect_client(self):
        pass

    def shutdown_server(self):
        pass
