from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpRequest
from pathlib import Path
import NetworkPackage.NetworkFunctions.Authorization as Authorization
import NetworkPackage.NetworkFunctions.Registration as Registration
import NetworkPackage.NetworkFunctions.UploadFile as UploadFile
import NetworkPackage.NetworkFunctions.SetPath as SetPath
import NetworkPackage.NetworkFunctions.GetFiles as GetFiles
import NetworkPackage.NetworkFunctions.RemoveFile as RemoveFiles
import NetworkPackage.NetworkFunctions.NextFolder as NextFolder
import NetworkPackage.NetworkFunctions.PrevFolder as PrevFolder
import NetworkPackage.NetworkFunctions.DownloadFile as DownloadFile
import NetworkPackage.NetworkFunctions.CreateFolder as CreateFolder


def index(request: HttpRequest):
    return render(request, "index.html")


def authorization(request: HttpRequest):
    if request.method == "POST":
        if "login" in request.session and "password" in request.session \
                and request.session["login"] == request.POST["login"] and request.session["password"] == request.POST["password"]:
            request.session["path"] = Path("Home").__str__()

            return HttpResponse("Авторизация прошла успешно")

        is_authorized, error_message = Authorization.authorization(request.POST["login"], request.POST["password"])

        if is_authorized:
            request.session["login"] = request.POST["login"]
            request.session["password"] = request.POST["password"]
            request.session["path"] = Path("Home").__str__()

            return HttpResponse("Авторизация прошла успешно")
        else:
            return HttpResponse(error_message)

    return redirect(index)


def registration(request: HttpRequest):
    if request.method == "POST":
        is_registered, error_message = Registration.registration(request.POST["login"], request.POST["password"])

        if is_registered:
            return HttpResponse("Регистрация прошла успешно")
        else:
            return HttpResponse(error_message)

    return redirect(index)


def upload_file(request: HttpRequest):
    if request.method == "POST":
        is_file_uploaded, error_message = UploadFile.upload_file(
            request.session["login"], request.session["password"], request.headers["File-Name"], UploadFile.from_hex(request.body.decode("ASCII")), request.session["path"]
            )

        if is_file_uploaded:
            return HttpResponse("Файл успешно загружен")
        else:
            return HttpResponse(error_message)

    return redirect(index)


def set_path(request: HttpRequest):
    if request.method == "POST":
        response = SetPath.set_path(request.session["login"], request.session["password"], request.session["path"])

        if response is None:
            return HttpResponse("Не удалось установить путь")
        else:
            # response contains list of FileData
            return HttpResponse("Успех")

    return redirect(index)


def get_files(request: HttpRequest):
    if request.method == "POST":
        response = GetFiles.get_files(request.session["login"], request.session["password"], request.session["path"])

        if response is None:
            return HttpResponse("Не удалось получить список файлов")
        elif type(response) == str:
            return HttpResponse(response)
        else:
            return HttpResponse("Успех")

    return redirect(index)


def remove_file(request: HttpRequest):
    if request.method == "POST":
        return HttpResponse(RemoveFiles.remove_file(request.session["login"], request.session["password"], request.session["path"], request.headers["File-Name"]))

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
        return HttpResponse(CreateFolder.create_folder(request.session["login"], request.session["password"], request.headers["Folder-Name"], request.session["path"]))

    return redirect(index)


def set_file_name(request: HttpRequest):
    if request.method == "POST":
        request.session["File-Name"] = request.headers["File-Name"]
        return HttpResponse("Успех")

    return redirect(index)
