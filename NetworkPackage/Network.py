import socket
from NetworkPackage.Constants import CLIENT_TIMEOUT_RECEIVE
from NetworkPackage.Constants import HTTP_PACKET_SIZE
from NetworkPackage.HTTPParser import HTTPParser


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

        size = 0
        last_packet = len(data)
        total_receive = 0

        while True:
            if last_packet == 0:
                raise RuntimeError("socket connection broken")

            total_receive += last_packet

            if total_receive > 25 and size == 0:
                parser = HTTPParser(data)

                size = int(parser.get_header("Total-HTTP-Message-Size"))

            if size == total_receive:
                break

            data += self._socket.recv(size - total_receive)

            last_packet = len(data) - last_packet

        return str(data.decode(encoding="CP1251"))

    def __del__(self):
        self._socket.close()
