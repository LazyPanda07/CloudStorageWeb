from NetworkPackage.Network import Network
from NetworkPackage.HTTPParser import HTTPParser
from NetworkPackage.HTTPBuilder import HTTPBuilder
from NetworkPackage.NetworkFunctions.Authorization import authorization

from NetworkPackage.Constants import *


def set_path(login: str, password: str, path: str, network: Network = None):
    if network is None:
        network = Network("31.207.166.231", 8500)
    response = None
    is_authorized, error_message = authorization(login, password, network)

    if is_authorized:
        body = "folder=" + path

        request = HTTPBuilder().set_method("POST"). \
            set_header(RequestType.CONTROL_TYPE, ControlRequests.SET_PATH). \
            set_header("Content-Length", len(body)). \
            build(body.encode("CP1251"))

        request = HTTPBuilder.insert_size_header_to_http_message(request)

        network.send(request.encode("CP1251"))

        response = HTTPParser(network.receive())

    return response
