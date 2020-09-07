@echo off

cd servers\APIServer
start APIServer.exe
cd..
cd..

cd servers\CloudStorageServer
start CloudStorageServer.exe
cd..
cd..

cd servers\DataBaseServer
start DataBaseServer.exe
cd..
cd..