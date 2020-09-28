from pathlib import Path

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpRequest
from django.http import HttpResponse

from NetworkPackage.Constants import Responses
from NetworkPackage.Constants import DATA_DELIMITER
from NetworkPackage.Constants import DATA_PART_DELIMITER

import NetworkPackage.NetworkFunctions.UploadFile as UploadFile
import NetworkPackage.NetworkFunctions.SetPath as SetPath
import NetworkPackage.NetworkFunctions.GetFiles as GetFiles
import NetworkPackage.NetworkFunctions.RemoveFile as RemoveFiles
import NetworkPackage.NetworkFunctions.NextFolder as NextFolder
import NetworkPackage.NetworkFunctions.PrevFolder as PrevFolder
import NetworkPackage.NetworkFunctions.DownloadFile as DownloadFile
import NetworkPackage.NetworkFunctions.CreateFolder as CreateFolder

import Conversions.HexConversions as HexConversions


def index(request: HttpRequest):
    if "login" not in request.session and "password" not in request.session:
        return redirect("..")

    return render(request, "storage.html")


def upload_file(request: HttpRequest):
    if request.method == "POST":
        is_file_uploaded, error_message = UploadFile.upload_file(
            request.session["login"], request.session["password"],
            HexConversions.from_hex_to_string(request.headers["File-Name"]),
            HexConversions.from_hex_to_binary(request.body.decode("ASCII")),
            request.session["path"]
            )

        if is_file_uploaded:
            return HttpResponse(Responses.OK_RESPONSE.value)
        else:
            return HttpResponse(error_message)

    return redirect(index)


def set_path(request: HttpRequest):
    if request.method == "POST":
        response = SetPath.set_path(request.session["login"], request.session["password"], request.session["path"])

        if response is None:
            return HttpResponse(Responses.FAIL_RESPONSE.value)
        else:
            return HttpResponse(Responses.OK_RESPONSE.value)

    return redirect(index)


def get_files(request: HttpRequest):
    if request.method == "POST":
        response = GetFiles.get_files(request.session["login"], request.session["password"], request.session["path"])

        if response is None:
            return HttpResponse(Responses.FAIL_RESPONSE.value)
        elif type(response) == str:
            return HttpResponse(response)
        else:
            files = []
            for i in response:
                files.append(i.file_name + DATA_PART_DELIMITER + i.file_extension)

            return HttpResponse("{}".format(DATA_DELIMITER).join(files))

    return redirect(index)


def remove_file(request: HttpRequest):
    if request.method == "POST":
        return HttpResponse(
            RemoveFiles.remove_file(
                request.session["login"], request.session["password"], request.session["path"],
                HexConversions.from_hex_to_string(request.headers["File-Name"])
                )
            )

    return redirect(index)


def next_folder(request: HttpRequest):
    if request.method == "POST":
        request.session["path"] = str(NextFolder.next_folder(request.headers["Folder-Name"], Path(request.session["path"])))

        return HttpResponse(request.session["path"])

    return redirect(index)


def prev_folder(request: HttpRequest):
    if request.method == "POST":
        request.session["path"] = str(PrevFolder.prev_folder(Path(request.session["path"])))

        return HttpResponse(request.session["path"])

    return redirect(index)


def download_file(request: HttpRequest):
    if request.method == "GET":
        response = HttpResponse(
            DownloadFile.download_file(request.session["login"], request.session["password"], request.session["File-Name"], request.session["path"]),
            content_type="application/octet-stream"
            )

        response["Content-Disposition"] = "inline; filename=" + request.session["File-Name"]

        return response

    return redirect(index)


def create_folder(request: HttpRequest):
    if request.method == "POST":
        return HttpResponse(
            CreateFolder.create_folder(
                request.session["login"], request.session["password"],
                HexConversions.from_hex_to_string(request.headers["Folder-Name"]),
                request.session["path"]
                )
            )

    return redirect(index)


def set_file_name(request: HttpRequest):
    if request.method == "POST":
        request.session["File-Name"] = request.headers["File-Name"]
        return HttpResponse(Responses.OK_RESPONSE.value)

    return redirect(index)


def log_out(request: HttpRequest):
    if request.method == "POST":
        if "login" in request.session:
            del request.session["login"]
        if "password" in request.session:
            del request.session["password"]

        return HttpResponse(Responses.OK_RESPONSE)

    return HttpResponse(Responses.FAIL_RESPONSE)
