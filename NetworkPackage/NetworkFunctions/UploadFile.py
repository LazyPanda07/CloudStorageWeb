from NetworkPackage.Network import Network
from NetworkPackage.HTTPParser import HTTPParser
from NetworkPackage.HTTPBuilder import HTTPBuilder

from NetworkPackage.Constants import *


def upload_file(file_name: str, file_data: bytes):
    network = Network("31.207.166.231", 8500)
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
