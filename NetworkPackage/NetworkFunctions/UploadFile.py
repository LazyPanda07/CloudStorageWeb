from NetworkPackage.Network import Network
from NetworkPackage.HTTPParser import HTTPParser
from NetworkPackage.HTTPBuilder import HTTPBuilder
from NetworkPackage.NetworkFunctions.SetPath import set_path

from NetworkPackage.Constants import APIServerIp
from NetworkPackage.Constants import APIServerPort
from NetworkPackage.Constants import FILE_PACKET_SIZE
from NetworkPackage.Constants import RequestType
from NetworkPackage.Constants import FilesRequests
from NetworkPackage.Constants import Responses


def upload_file(login: str, password: str, file_name: str, file_data: bytes, path: str):
    with Network(APIServerIp, APIServerPort) as network:
        is_path_set = set_path(login, password, path, network)

        if is_path_set is not None and is_path_set == Responses.OK_RESPONSE.value:
            offset = 0
            file_data_size = len(file_data)
            data = bytes()
            is_last = False

            while True:
                if file_data_size - offset >= FILE_PACKET_SIZE:
                    data = file_data[offset:FILE_PACKET_SIZE]
                else:
                    data = file_data[offset:]

                    is_last = True

                message = HTTPBuilder().set_method("POST"). \
                    set_header(RequestType.FILES_TYPE, FilesRequests.UPLOAD_FILE). \
                    set_header("File-Name", file_name). \
                    set_header("Range", offset). \
                    set_header("Content-Length", len(data)). \
                    set_header("Total-File-Size" if is_last else "Reserved", file_data_size if is_last else 0). \
                    build(data)

                message = HTTPBuilder.insert_size_header_to_http_message(message)

                network.send(message)

                offset += len(data)

                if is_last:
                    break

            response = HTTPParser(network.receive())

            return response.get_header("Error") == "0", response.get_body().decode("CP1251")

        return False, "Не удалось загрузить файл"
