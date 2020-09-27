from enum import Enum


class HTTPBuilder:
    _http_version = "HTTP/1.1"
    _custom_http_header_size = "Total-HTTP-Message-Size: "

    @staticmethod
    def _calculate_http_message_size(http_message: str):
        i_size = len(http_message) + len(HTTPBuilder._custom_http_header_size) + 2
        s_size = str(i_size)
        i_size += len(s_size)
        s_size = str(i_size)

        return s_size

    @staticmethod
    def insert_size_header_to_http_message(http_message: str):
        total_http_message_size = HTTPBuilder._custom_http_header_size + HTTPBuilder._calculate_http_message_size(http_message) + "\r\n"
        find_rn = http_message.find("\r\n")

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
        result = str()

        if len(self._method) == 0:
            result = self._http_version + " " + self._responseCode + "\r\n" + self._headers
        else:
            if len(self._parameters) == 0:
                self._parameters = "/"

            result = self._method + " " + self._parameters + " " + self._http_version + "\r\n" + self._headers

        if len(body) != 0:
            result = result + "\r\n" + body.decode("CP1251")

        return result
