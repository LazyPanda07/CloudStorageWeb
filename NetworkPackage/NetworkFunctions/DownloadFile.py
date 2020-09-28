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


def download_file(login: str, password: str, file_name: str, path: str):
    with Network(APIServerIp, APIServerPort) as network:
        is_path_set = set_path(login, password, path, network)
        total_file_size = 0
        data = []
        offset = 0

        if is_path_set is not None and is_path_set.get_body() == b"OK":
            while True:
                request = HTTPBuilder().set_method("POST"). \
                    set_header(RequestType.FILES_TYPE, FilesRequests.DOWNLOAD_FILE). \
                    set_header("File-Name", file_name). \
                    set_header("Range", offset) \
                    .build()

                request = HTTPBuilder.insert_size_header_to_http_message(request)

                network.send(request)

                response = HTTPParser(network.receive())

                total_file_size = response.get_header("Total-File-Size")

                data.append(response.get_body())

                offset += len(data[-1])

                if total_file_size is not None:
                    break

            return b''.join(data)

        return "Не удалось скачать файл"
