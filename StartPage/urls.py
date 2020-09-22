from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("authorization", views.authorization, name="authorization"),
    path("registration", views.registration, name="registration"),
    path("uploadFile", views.upload_file, name="upload_file"),
    path("setPath", views.set_path, name="set_path"),
    path("getFiles", views.get_files, name="get_files"),
    path("removeFile", views.remove_file, name="remove_file"),
    path("nextFolder", views.next_folder, name="next_folder"),
    path("prevFolder", views.prev_folder, name="prev_folder"),
    path("downloadFile", views.download_file, name="download_file"),
    path("setFileName", views.set_file_name, name="set_file_name"),
    ]
