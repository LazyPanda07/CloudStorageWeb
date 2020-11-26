from NetworkPackage.Network import Network
from NetworkPackage.HTTPParser import HTTPParser
from NetworkPackage.HTTPBuilder import HTTPBuilder
from NetworkPackage.NetworkFunctions.SetPath import set_path

from NetworkPackage.Constants import APIServerIp
from NetworkPackage.Constants import APIServerPort
from NetworkPackage.Constants import RequestType
from NetworkPackage.Constants import FilesRequests
from NetworkPackage.Constants import Responses


def remove_file(login: str, password: str, path: str, file_name: str):
    with Network(APIServerIp, APIServerPort) as network:
        is_path_set = set_path(login, password, path, network)

        if is_path_set is not None and is_path_set == Responses.OK_RESPONSE.value:
            request = HTTPBuilder().set_method("POST"). \
                set_header(RequestType.FILES_TYPE, FilesRequests.REMOVE_FILE). \
                set_header("File-Name", file_name). \
                build()

            request = HTTPBuilder.insert_size_header_to_http_message(request)

            network.send(request)

            response = HTTPParser(network.receive())

            if response.get_header("Error") == "1":
                return "Не удалось удалить файл"
            else:
                return "Файл успешно удален"

        return "Не удалось удалить файл"
