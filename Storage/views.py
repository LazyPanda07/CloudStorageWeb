from pathlib import Path

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpRequest
from django.http import HttpResponse

from NetworkPackage.Constants import Responses

import NetworkPackage.NetworkFunctions.UploadFile as UploadFile
import NetworkPackage.NetworkFunctions.SetPath as SetPath
import NetworkPackage.NetworkFunctions.GetFiles as GetFiles
import NetworkPackage.NetworkFunctions.RemoveFile as RemoveFiles
import NetworkPackage.NetworkFunctions.NextFolder as NextFolder
import NetworkPackage.NetworkFunctions.PrevFolder as PrevFolder
import NetworkPackage.NetworkFunctions.DownloadFile as DownloadFile
import NetworkPackage.NetworkFunctions.CreateFolder as CreateFolder


def index(request: HttpRequest):
    if "login" not in request.session and "password" not in request.session:
        return redirect("..")

    return render(request, "storage.html")


def upload_file(request: HttpRequest):
    if request.method == "POST":
        is_file_uploaded, error_message = UploadFile.upload_file(
            request.session["login"], request.session["password"], request.headers["File-Name"], UploadFile.from_hex(request.body.decode("ASCII")), request.session["path"]
            )

        if is_file_uploaded:
            return HttpResponse(Responses.OK_RESPONSE.value)
        else:
            return HttpResponse(error_message)

    return render(request, "storage.html")


def set_path(request: HttpRequest):
    if request.method == "POST":
        response = SetPath.set_path(request.session["login"], request.session["password"], request.session["path"])

        if response is None:
            return HttpResponse(Responses.FAIL_RESPONSE.value)
        else:
            # response contains list of FileData
            return HttpResponse(Responses.OK_RESPONSE.value)

    return render(request, "storage.html")


def get_files(request: HttpRequest):
    if request.method == "POST":
        response = GetFiles.get_files(request.session["login"], request.session["password"], request.session["path"])

        if response is None:
            return HttpResponse(Responses.FAIL_RESPONSE.value)
        elif type(response) == str:
            return HttpResponse(response)
        else:
            return HttpResponse(Responses.OK_RESPONSE.value)

    return render(request, "storage.html")


def remove_file(request: HttpRequest):
    if request.method == "POST":
        return HttpResponse(RemoveFiles.remove_file(request.session["login"], request.session["password"], request.session["path"], request.headers["File-Name"]))

    return render(request, "storage.html")


def next_folder(request: HttpRequest):
    if request.method == "POST":
        request.session["path"] = str(NextFolder.next_folder(request.headers["Folder-Name"], Path(request.session["path"])))

        return HttpResponse(request.session["path"])

    return render(request, "storage.html")


def prev_folder(request: HttpRequest):
    if request.method == "POST":
        request.session["path"] = str(PrevFolder.prev_folder(Path(request.session["path"])))

        return HttpResponse(request.session["path"])

    return render(request, "storage.html")


def download_file(request: HttpRequest):
    if request.method == "GET":
        response = HttpResponse(
            DownloadFile.download_file(request.session["login"], request.session["password"], request.session["File-Name"], request.session["path"]),
            content_type="application/octet-stream"
            )

        response["Content-Disposition"] = "inline; filename=" + request.session["File-Name"]

        return response

    return render(request, "storage.html")


def create_folder(request: HttpRequest):
    if request.method == "POST":
        return HttpResponse(CreateFolder.create_folder(request.session["login"], request.session["password"], request.headers["Folder-Name"], request.session["path"]))

    return render(request, "storage.html")


def set_file_name(request: HttpRequest):
    if request.method == "POST":
        request.session["File-Name"] = request.headers["File-Name"]
        return HttpResponse(Responses.OK_RESPONSE.value)

    return render(request, "storage.html")
