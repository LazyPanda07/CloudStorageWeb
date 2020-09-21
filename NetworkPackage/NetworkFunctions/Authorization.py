from NetworkPackage.Network import Network
from NetworkPackage.HTTPParser import HTTPParser
from NetworkPackage.HTTPBuilder import HTTPBuilder

from NetworkPackage.Constants import *


def authorization(login: str, password: str, network: Network = None):
    is_network_not_passed = network is None

    if is_network_not_passed:
        network = Network("31.207.166.231", 8500)
    body = "login={}&password={}".format(login, password)

    request = HTTPBuilder().set_method("POST"). \
        set_header(RequestType.ACCOUNT_TYPE, AccountRequests.AUTHORIZATION). \
        set_header("Content-Length", str(len(body))). \
        build(body.encode("ASCII"))

    request = HTTPBuilder.insert_size_header_to_http_message(request)

    network.send(request.encode("ASCII"))

    response = HTTPParser(network.receive())

    if is_network_not_passed:
        network.close()

    return response.get_header("Error") == "0", response.get_body().decode("CP1251")
