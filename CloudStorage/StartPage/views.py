from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpRequest
import NetworkPackage.NetworkFunctions.Authorization as Authorization
import NetworkPackage.NetworkFunctions.Registration as Registration


def index(request: HttpRequest):
    return render(request, "index.html")


def authorization(request: HttpRequest):
    if request.method == "POST":
        is_authorized, error_message = Authorization.authorization(request.POST["login"], request.POST["password"])

        if is_authorized:
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
