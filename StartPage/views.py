from django.shortcuts import render
from NetworkPackage.Network import Network
from NetworkPackage.HTTPBuilder import HTTPBuilder
from NetworkPackage.Constants import *


def index(request):
    return render(request, "index.html")
