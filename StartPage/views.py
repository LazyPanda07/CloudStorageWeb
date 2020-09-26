from pathlib import Path

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpRequest

from Storage.views import index as storage_index

from NetworkPackage.Constants import Responses

import NetworkPackage.NetworkFunctions.Authorization as Authorization
import NetworkPackage.NetworkFunctions.Registration as Registration


def index(request: HttpRequest):
    if "login" in request.session and "password" in request.session:
        is_authorized, error_message = Authorization.authorization(request.session["login"], request.session["password"])

        if is_authorized:
            request.session["path"] = "Home"
            return redirect(storage_index)
        else:
            del request.session["login"]
            del request.session["password"]
            if "path" in request.session:
                del request.session["path"]

    return render(request, "index.html")


def authorization(request: HttpRequest):
    if request.method == "POST":
        if "login" in request.session and "password" in request.session \
                and request.session["login"] == request.POST["login"] and request.session["password"] == request.POST["password"]:
            request.session["path"] = Path("Home").__str__()

            return HttpResponse(Responses.OK_RESPONSE.value)

        is_authorized, error_message = Authorization.authorization(request.POST["login"], request.POST["password"])

        if is_authorized:
            request.session["login"] = request.POST["login"]
            request.session["password"] = request.POST["password"]
            request.session["path"] = Path("Home").__str__()

            return HttpResponse(Responses.OK_RESPONSE.value)
        else:
            return HttpResponse(error_message)

    return redirect(index)


def registration(request: HttpRequest):
    if request.method == "POST":
        is_registered, error_message = Registration.registration(request.POST["login"], request.POST["password"])

        if is_registered:
            return HttpResponse(Responses.OK_RESPONSE.value)
        else:
            return HttpResponse(error_message)

    return redirect(index)
