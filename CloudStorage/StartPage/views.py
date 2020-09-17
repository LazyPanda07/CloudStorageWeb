from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpRequest
import NetworkPackage.NetworkFunctions.Authorization as Authorization


def index(request):
    return render(request, "index.html")


def authorization(request: HttpRequest):
    if request.method == "POST":
        is_authorized, error_message = Authorization.authorization(request.POST["login"], request.POST["password"])

        if is_authorized:
            return HttpResponse("Авторизация прошла успешно")
        else:
            return HttpResponse(error_message)

    return redirect(index)
