from enum import Enum

GET_FILE = 1

APIServerIp = ""
APIServerPort = -1

HTTP_PACKET_SIZE = 4096
FILE_PACKET_SIZE = 10 * 1024 * 1024  # 10 MB

CLIENT_TIMEOUT_RECEIVE = 30  # 30 seconds

DATA_DELIMITER = "/"
DATA_PART_DELIMITER = "|"
WINDOWS_SEPARATOR = '\\'


class RequestType(Enum):
    ACCOUNT_TYPE = "Account-Request"
    FILES_TYPE = "Files-Request"
    EXIT_TYPE = "Exit-Request"
    CANCEL_TYPE = "Cancel-Request"
    CONTROL_TYPE = "Control-Request"


class NetworkRequests(Enum):
    EXIT = "EOSS"
    CANCEL_OPERATION = "Cancel-Operation"


class ControlRequests(Enum):
    NEXT_FOLDER = "Next-Folder"
    PREVIOUS_FOLDER = "Previous-Folder"
    SET_PATH = "Set-Path"


class AccountRequests(Enum):
    AUTHORIZATION = "Authorization"
    REGISTRATION = "Registration"
    SET_LOGIN = "Set-Login"


class FilesRequests(Enum):
    UPLOAD_FILE = "Upload-File"
    DOWNLOAD_FILE = "Download-File"
    SHOW_ALL_FILES_IN_DIRECTORY = "Show-All-Files-In-Folder"
    REMOVE_FILE = "Remove-File"
    CREATE_FOLDER = "Create-Folder"


class Responses(Enum):
    OK_RESPONSE = "OK"
    FAIL_RESPONSE = "FAIL"
    UNKNOWN_REQUEST = "Unknown request"
