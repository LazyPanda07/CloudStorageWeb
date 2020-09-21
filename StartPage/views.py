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
        is_file_uploaded, error_message = UploadFile.upload_file(request.session["login"], request.session["password"], request.headers["File-Name"], request.body)

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
