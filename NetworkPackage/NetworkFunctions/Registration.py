from NetworkPackage.Network import Network
from NetworkPackage.HTTPParser import HTTPParser
from NetworkPackage.HTTPBuilder import HTTPBuilder

from NetworkPackage.Constants import *


def registration(login: str, password: str):
    with Network(APIServerIp, APIServerPort) as network:
        body = "login={}&password={}".format(login, password)

        request = HTTPBuilder().set_method("POST"). \
            set_header(RequestType.ACCOUNT_TYPE, AccountRequests.REGISTRATION). \
            set_header("Content-Length", str(len(body))). \
            build(body.encode("ASCII"))

        request = HTTPBuilder.insert_size_header_to_http_message(request)

        network.send(request.encode("ASCII"))

        response = HTTPParser(network.receive())

        return response.get_header("Error") == "0", response.get_body().decode("CP1251")
