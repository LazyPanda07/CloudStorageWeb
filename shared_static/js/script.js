$.ajaxSetup({
    beforeSend: function (xhr, settings)
    {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});

function fromBinaryToHex(/** uint8 */ byte)
{
    result = byte.toString(16)

    if (result.length == 1) {
        result = "0" + result;
    }

    return result;
}

function fromStringToHex(/** String */ string)
{
    let result = new String();

    for (const i of string) {
        tem = (i.charCodeAt(0)).toString(16);

        if (tem.length != 3) {
            newString = new String();

            for (let i = 0; i < 3 - tem.length; i++) {
                newString += "0";
            }

            tem = newString + tem;
        }

        result += tem;
    }

    return result;
}

function authorization(/** string */ login, /** string */ password)
{
    return $.post(
        {
            url: "/authorization",
            dataType: "text",
            data: "login=" + login + "&password=" + password,
            success: function (data)
            {
                return data;
            }
        }
    );
}

function registration(/** string */ login, /** string */ password)
{
    return $.post(
        {
            url: "/registration",
            dataType: "text",
            data: "login=" + login + "&password=" + password,
            success: function (data)
            {
                return data;
            }
        }
    );
}

var filesToUpload;

function uploadFiles(/** File[] */ files, /** int */ currentIndex)
{
    if (files.length == currentIndex) {
        window.location.href = "/storage";
        return;
    }

    let reader = new FileReader();

    reader.addEventListener("load", (event) =>
    {
        let data = new Uint8Array(event.target.result);
        let binaryString = "";
        fileName = fromStringToHex(files[currentIndex].name);

        for (const i of data) {
            binaryString += fromBinaryToHex(i);
        }

        console.log(fileName);

        $.post(
            {
                url: "uploadFile",
                headers: { "File-Name": fileName },
                data: binaryString,
                success: function (data)
                {
                    return data;
                }
            }
        ).then((result) =>
        {
            uploadFiles(files, currentIndex + 1);
        }).catch((err) =>
        {
            console.log(err);
        });
    });

    reader.readAsArrayBuffer(files[currentIndex]);
}

function setPath()
{
    return $.post(
        {
            url: "/setPath",
            dataType: "text",
            success: function (data)
            {
                alert(data);
            }
        }
    );
}

function getFiles()
{
    return $.post(
        {
            url: "getFiles",
            dataType: "text",
            success: function (data)
            {
                return data;
            }
        }
    );
}

function removeFile(/** String */ fileName)
{
    return $.post(
        {
            url: "removeFile",
            headers: { "File-Name": fromStringToHex(fileName) },
            dataType: "text",
            success: function (data)
            {
                return data;
            }
        }
    );
}

function nextFolder(/** String */ folderName)
{
    return $.post(
        {
            url: "/nextFolder",
            headers: { "Folder-Name": folderName },
            dataType: "text",
            success: function (data)
            {
                alert(data);
            }
        }
    );
}

function prevFolder()
{
    return $.post(
        {
            url: "/prevFolder",
            dataType: "text",
            success: function (data)
            {
                alert(data);
            }
        }
    );
}

function downloadFile(/** String */ fileName)
{
    $.post(
        {
            url: "setFileName",
            dataType: "text",
            headers: { "File-Name": fromStringToHex(fileName) },
            success: function (data)
            {
                console.log(data);
            }
        }
    ).then(() =>
    {
        window.location = "downloadFile";
    });
}

function createFolder(/** String */ folderName)
{
    return $.post(
        {
            url: "createFolder",
            dataType: "text",
            headers: { "Folder-Name": fromStringToHex(folderName) },
            success: function (data)
            {
                console.log(data);
            }
        }
    );
}

function logOut()
{
    $.post(
        {
            url: "logOut",
            dataType: "text",
            async: false,
            success: function (data)
            {
                return data
            }
        }
    );

    return true;
}

function takeFilesFromInput()
{
    filesToUpload = this.files;
    uploadButton.disabled = true;

    uploadFiles(filesToUpload, 0);
}

function createFolderElement(/** String */ folderName)
{
    return String.raw
        `<div class="listing__item">
            <img src="/static/img/icons/folder.svg" alt="">
            <span>${folderName}</span>
        </div>`;
}

function createFileElement(/** String */ fileName)
{
    return String.raw
        `<div class="listing__item">
            <img src="/static/img/icons/file.svg" alt="">
            <span>${fileName}</span>
        </div>`;
}

/*
let listItem = document.querySelector('.listing__item'),
    popupItem = document.querySelector('.popup-file'),
    contentArea = document.getElementById('content-area')


listItem.addEventListener('click',
    function () {
    popupItem.style.display = "flex";
    this.style.border = "2px solid #0071F5";
    this.style.borderRadius = "10px"
});*/

let regBtn = document.querySelector('.header__reg-btn');
let authBtn = document.querySelector('.body__auth-btn');
let regBtnClose = document.querySelector('.reg-popup__close');
let authBtnClose = document.querySelector('.auth-popup__close');
let regPopup = document.querySelector('.reg-popup');
let authPopup = document.querySelector('.auth-popup');
let uploadButton = document.getElementById("upload-file");

if (regBtn) {
    regBtn.addEventListener("click", function ()
    {
        regPopup.style.display = "block";
        authPopup.style.display = "none";
    });
}

if (regBtnClose) {
    regBtnClose.addEventListener("click", function ()
    {
        regPopup.style.display = "none";
    });
}

if (authBtn) {
    authBtn.addEventListener("click", function ()
    {
        authPopup.style.display = "block";
        regPopup.style.display = "none";
    });
}

if (authBtnClose) {
    authBtnClose.addEventListener("click", function ()
    {
        authPopup.style.display = "none";
    });
}

$("#log-in").click(function ()
{
    authorization($("#authorization-login").val(), $("#authorization-password").val()).then(function (data)
    {
        if (data == "OK") {
            authPopup.style.display = "none";

            window.location.href = "/storage";
        }
        else {
            alert(data);
        }
    });
});

$("#register").click(function ()
{
    let password = $("#registration-password").val();
    let repeatPassword = $("#registration-repeat-password").val();

    if (password == repeatPassword) {
        registration($("#registration-login").val(), password).then(function (data)
        {
            if (data == "OK") {
                alert("Регистрация прошла успешно");

                regPopup.style.display = "none";
            }
            else {
                alert(data);
            }
        });
    }
});

$("#create-folder").click(function ()
{
    let folderName = prompt("Введите название новой папки");

    createFolder(folderName).then(() => window.location.href = "/storage");
});

$(document).ready(function ()
{
    getFiles().then(function (data)
    {
        if (data == "Эта папка пуста") {
            return;
        }

        let allFiles = $("#all-files");
        let fileNames = data.split('/');

        for (const i of fileNames) {
            tem = i.split('|');

            if (tem[1] == "Папка с файлами") {
                allFiles.append(createFolderElement(tem[0]));
            }
            else {
                allFiles.append(createFileElement(tem[0]));
            }
        }
    });
});

document.getElementById("all-files").addEventListener("dragover", (event) =>
{
    event.stopPropagation();
    event.preventDefault();

    event.dataTransfer.dropEffect = 'copy';
});

document.getElementById("all-files").addEventListener("drop", (event) =>
{
    event.stopPropagation();
    event.preventDefault();

    uploadFiles(event.dataTransfer.files, 0);
});

if (uploadButton) {
    uploadButton.addEventListener("change", takeFilesFromInput, false);
}