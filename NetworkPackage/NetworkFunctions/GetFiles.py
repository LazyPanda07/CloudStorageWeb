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
from NetworkPackage.Constants import Responses

from FileData.FileData import FileData


def get_files(login: str, password: str, path: str):
    with Network(APIServerIp, APIServerPort) as network:
        data = None
        is_path_set = set_path(login, password, path, network)

        if is_path_set is not None and is_path_set == Responses.OK_RESPONSE.value:
            request = HTTPBuilder().set_method("POST"). \
                set_header(RequestType.FILES_TYPE, FilesRequests.SHOW_ALL_FILES_IN_DIRECTORY). \
                build()

            request = HTTPBuilder.insert_size_header_to_http_message(request)

            network.send(request)

            response = HTTPParser(network.receive())

            if response.get_header("Error") == "1":
                return response.get_body().decode("CP1251")

            body = response.get_body().decode("CP1251")
            data = []
            tem = [[] for _ in range(6)]
            cur_index = 0

            for i in body:
                if i == DATA_DELIMITER[0]:
                    data.append(FileData(''.join(tem[0]), ''.join(tem[1]), ''.join(tem[2]), ''.join(tem[3]), ''.join(tem[4]), int(''.join(tem[5]))))

                    cur_index = 0
                    tem = [[] for _ in range(6)]

                elif i == DATA_PART_DELIMITER[0]:
                    cur_index += 1
                else:
                    tem[cur_index].append(i)

        return data
