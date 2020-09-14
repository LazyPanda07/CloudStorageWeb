class HTTPParser:
    _message = None
    _headers = None
    _parameters = None
    _body = None

    def __init__(self, data: bytes):
        self._headers = dict()
        self._method = str()
        self._body = bytes()
        is_contains_body = data.find(b"\r\n\r\n") != -1

        if is_contains_body:
            self._message = str(data[:data.rfind(b"\r\n\r\n")].decode("CP1251"))
            self._body = data[data.rfind(b"\r\n\r\n") + 4:]
            http_message = str(data[data.find(b"\r\n") + 2:data.rfind(b"\r\n\r\n")].decode("CP1251"))
        else:
            self._message = str(data.decode("CP1251"))
            http_message = str(data[data.find(b"\r\n") + 2:data.rfind(b"\r\n")].decode("CP1251"))

        for i in http_message.split("\r\n"):
            tem = i.split(": ")
            self._headers[tem[0]] = tem[1]

        parameters_start = data.find(b'/') + 1
        parameters_end = data.find(b' ', parameters_start)

        self._parameters = str(data[parameters_start:parameters_end].decode(encoding="CP1251"))

    def get_parameters(self):
        return self._parameters

    def get_headers(self):
        return self._headers

    def get_header(self, key: str):
        return self._headers.get(key, None)

    def get_body(self):
        return self._body

    def get_message(self):
        return self._message
