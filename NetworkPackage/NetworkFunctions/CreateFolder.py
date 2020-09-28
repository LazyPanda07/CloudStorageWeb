from NetworkPackage.Network import Network
from NetworkPackage.HTTPParser import HTTPParser
from NetworkPackage.HTTPBuilder import HTTPBuilder
from NetworkPackage.NetworkFunctions.SetPath import set_path

from NetworkPackage.Constants import APIServerIp
from NetworkPackage.Constants import APIServerPort
from NetworkPackage.Constants import DATA_PART_DELIMITER
from NetworkPackage.Constants import DATA_DELIMITER
from NetworkPackage.Constants import RequestType
from NetworkPackage.Constants import FilesRequests


def create_folder(login: str, password: str, folder_name: str, path: str):
    with Network(APIServerIp, APIServerPort) as network:
        is_path_set = set_path(login, password, path, network)

        if is_path_set is not None and is_path_set.get_body() == b"OK":
            body = "folder=" + folder_name

            request = HTTPBuilder().set_method("POST"). \
                set_header(RequestType.FILES_TYPE, FilesRequests.CREATE_FOLDER). \
                set_header("Content-Length", len(body)). \
                build(body.encode("CP1251"))

            request = HTTPBuilder.insert_size_header_to_http_message(request)

            network.send(request)

            response = HTTPParser(network.receive())

            return "Папка успешно создана" if response.get_header("Error") == "0" else "Не удалось создать папку"

        return "Не удалось создать папку"
