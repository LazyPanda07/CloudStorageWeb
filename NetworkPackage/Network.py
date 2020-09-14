import socket
from NetworkPackage.Constants import CLIENT_TIMEOUT_RECEIVE
from NetworkPackage.Constants import HTTP_PACKET_SIZE


class Network:
    _socket = None

    def __init__(self, ip: str, port: int):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

        self._socket.settimeout(CLIENT_TIMEOUT_RECEIVE)

        self._socket.connect((ip, port))

    def send(self, message: str):
        data = message.encode(encoding="CP1251")
        total_sent = 0

        while total_sent < len(data):
            last_packet = self._socket.send(data[total_sent:])

            if last_packet == 0:
                raise RuntimeError("socket connection broken")

            total_sent = total_sent + last_packet

        return total_sent

    def receive(self):
        data = self._socket.recv(HTTP_PACKET_SIZE)

        return str(data.decode(encoding="CP1251"))

    def __del__(self):
        self._socket.close()
