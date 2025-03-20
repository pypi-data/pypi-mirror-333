import socket
import threading
import time

class ATCP:
    """
    Main ATCP class. Init: `ATCP(socket.socket())`.
    """
    def __init__(self, sock):
        self.socket = sock
        self.connected = False
        self.ping_interval = 10  # seconds
        self.server_mode = False
        self.host = None
        self.port = None
        self.path = None
        self.messages = []

    def bind(self, address):
        """
        Only for server! Bind to address. Example: `atcp.bind(("0.0.0.0", 1614))`.
        """
        self.host, self.port = address
        self.socket.bind((self.host, self.port))
        self.server_mode = True

    def listen(self, backlog=1):
        """
        Only for server! Listen connections. Example: `atcp.listen(10)`
        """
        if not self.server_mode:
            raise ValueError("Cannot listen without binding")
        self.socket.listen(backlog)

    def accept(self):
        """
        Only for server! Accept Connection. Example: `client = atcp.accept()`
        """
        if not self.server_mode:
            raise ValueError("Cannot accept connections without listening")
        client_socket, address = self.socket.accept()
        atcp = ATCP(client_socket)
        atcp.host, atcp.port = address
        atcp.connected = True
        threading.Thread(target=atcp.handle_client).start()
        return atcp

    def connect(self, address, path=''):
        """
        Only for client! Connect to server. Example: `atcp.connect(("localhost",1614), "/test")``
        """
        self.host, self.port = address
        self.path = path
        self.socket.connect((self.host, self.port))
        self.send_packet('PATH ' + self.path)
        response = self.recv_packet()
        if response.startswith('CONN 0'):
            self.connected = True
            threading.Thread(target=self.ping_thread).start()
        else:
            self.close()

    def send_packet(self, packet):
        """
        System
        """
        self.socket.sendall(packet.encode() + b'\n')

    def recv_packet(self):
        """
        System
        """
        return self.socket.recv(1024).decode().strip()

    def ping_thread(self):
        """
        System
        """
        while self.connected:
            self.send_packet('PING')
            response = self.recv_packet()
            if response == 'PONG':
                time.sleep(self.ping_interval)
            elif response == 'CLOSE':
                self.close()
                break

    def send_message(self, message):
        """
        Send message. Example: `atcp.send_message("Hello!")`
        """
        self.send_packet('MESSAGE ' + message)

    def close(self):
        """
        Close connection. Example: `atcp.close()`
        """
        if self.connected:
            self.send_packet('CLOSE')
            self.socket.close()
            self.connected = False

    def handle_client(self):
        """
        System
        """
        while self.connected:
            try:
                message = self.recv_packet()
            except OSError:
                break
            if message.startswith('PING'):
                self.send_packet('PONG')
            elif message.startswith('CLOSE'):
                self.close()
            elif message.startswith('MESSAGE '):
                print(message[8:])
                self.messages.append(message[8:])
            elif message.startswith('PATH '):
                self.send_packet('CONN 0')
                print('Client connected with path:', message[5:])
                self.path = message[5:]

def parse_atcp_url(url):
    """
    Parse ATCP URL. Example: `host, port, path = parse_atcp_url("atcp://example.com:1614/test")`
    """
    import urllib.parse
    parsed_url = urllib.parse.urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port or 1614
    path = parsed_url.path
    return host, port, path
