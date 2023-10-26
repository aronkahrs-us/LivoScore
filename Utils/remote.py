import threading
import asyncio
import websockets


class Remote:
    def __init__(self, window) -> None:
        self.window = window
        # Server data
        self.port = 7890

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        print("Server listening on Port " + str(self.port))
        self.connected = set()
        start_server = websockets.serve(self.echo, "localhost", self.port)
        loop.run_until_complete(start_server)
        loop.run_forever()

    async def echo(self, websocket, path):
        # Store a copy of the connected client
        self.connected.add(websocket)
        # Handle incoming messages
        try:
            async for message in websocket:
                print("Received message from client: " + message)
                if message == "Start Match":
                    self.start_match(6000)
                elif message == "Stop Match":
                    self.stop_match()
                # Send a response to all connected clients except sender
                for conn in self.connected:
                    if conn != websocket:
                        await conn.send("Someone said: " + message)
        # Handle disconnecting clients
        except websockets.exceptions.ConnectionClosed as e:
            print("A client just disconnected")
        finally:
            self.connected.remove(websocket)

    async def send_update(self, websocket, data):
        try:
            for conn in self.connected:
                if conn != websocket:
                    await conn.send(data)
        except websockets.exceptions.ConnectionClosed as e:
            print("Error sending Update",e)

    def start_match(self, m_id):
        self.window["-ID-"].update(value="PE\u00d1AROL vs CBPS")
        self.window.write_event_value("-ST-", 0)
        pass

    def stop_match(self):
        self.window.write_event_value("-ST-", 0)
        pass
