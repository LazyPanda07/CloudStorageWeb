import socket
from NetworkPackage.Constants import CLIENT_TIMEOUT_RECEIVE
from NetworkPackage.Constants import HTTP_PACKET_SIZE
from NetworkPackage.Constants import RequestType
from NetworkPackage.Constants import NetworkRequests
from NetworkPackage.HTTPParser import HTTPParser
from NetworkPackage.HTTPBuilder import HTTPBuilder


class Network:
    def __init__(self, ip: str, port: int):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

        self._socket.settimeout(CLIENT_TIMEOUT_RECEIVE)

        self._socket.connect((ip, port))

    def send(self, data: bytes):
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

        while True:
            if last_packet == 0:
                raise RuntimeError("socket connection broken")

            if len(data) > 25 and size == 0:
                parser = HTTPParser(data)

                size = int(parser.get_header("Total-HTTP-Message-Size"))

            if size == len(data):
                break

            data += self._socket.recv(size - len(data))

            last_packet = len(data) - last_packet

        return data

    def close(self):
        end_of_socket_stream = HTTPBuilder().set_method("POST"). \
            set_header(RequestType.EXIT_TYPE, NetworkRequests.EXIT). \
            build()

        end_of_socket_stream = HTTPBuilder.insert_size_header_to_http_message(end_of_socket_stream)

        self.send(end_of_socket_stream)

        self._socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
