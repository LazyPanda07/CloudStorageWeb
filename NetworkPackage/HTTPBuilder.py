from enum import Enum


class HTTPBuilder:
    _http_version = "HTTP/1.1"
    _custom_http_header_size = "Total-HTTP-Message-Size: "

    @staticmethod
    def _calculate_http_message_size(http_message: bytes):
        i_size = len(http_message) + len(HTTPBuilder._custom_http_header_size) + 2
        s_size = str(i_size)
        i_size += len(s_size)
        s_size = str(i_size)

        return s_size

    @staticmethod
    def insert_size_header_to_http_message(http_message: bytes):
        total_http_message_size = HTTPBuilder._custom_http_header_size.encode(
            "CP1251") + HTTPBuilder._calculate_http_message_size(http_message).encode("CP1251") + b"\r\n"
        find_rn = http_message.find(b"\r\n")

        return http_message[:find_rn + 2] + total_http_message_size + http_message[find_rn + 2:]

    def __init__(self):
        self._method = str()
        self._parameters = str()
        self._responseCode = str()
        self._headers = str()

    def set_method(self, method: str):
        self._method = method

        return self

    def set_parameters(self, parameters: str):
        self._method = str(parameters.encode(encoding="CP1251"))

        return self

    def set_response_code(self, response_code: str):
        self._responseCode = response_code

        return self

    def set_header(self, name, value):
        if isinstance(name, Enum):
            self._headers += name.value + ": "
        else:
            self._headers += str(name) + ": "

        if isinstance(value, Enum):
            self._headers += str(value.value.encode("CP1251"), encoding="CP1251") + "\r\n"
        elif type(value) == str:
            self._headers += str(value.encode("CP1251"), encoding="CP1251") + "\r\n"
        else:
            self._headers += str(value) + "\r\n"

        return self

    def build(self, body=bytes()):
        if len(self._method) == 0:
            result = self._http_version.encode("CP1251") + b" " + self._responseCode.encode(
                "CP1251") + b"\r\n" + self._headers.encode("CP1251")
        else:
            if len(self._parameters) == 0:
                self._parameters = "/"

            result = self._method.encode("CP1251") + b" " + self._parameters.encode(
                "CP1251") + b" " + self._http_version.encode("CP1251") + b"\r\n" + self._headers.encode("CP1251")

        result = result + b"\r\n"

        if len(body) != 0:
            result = result + body

        return result
