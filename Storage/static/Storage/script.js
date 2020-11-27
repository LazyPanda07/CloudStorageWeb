$.ajaxSetup({
    beforeSend: function (xhr, settings)
    {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
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

/**
 * 
 * @param {type} progressBarPercentWidth float
 * @param {type} fileName String
 */
function uploadFileNotify(progressBarPercentWidth, fileName)
{
    let progressBar = document.getElementById("progressBar");
    let fileInformation = document.getElementById("fileInformation");

    fileInformation.innerHTML = "Загрузка файла " + fileName;

    progressBar.style.width = progressBarPercentWidth + "%";
    progressBar.innerHTML = progressBarPercentWidth + "%";
}

/**
 * 
 * @param {type} byte uint8
 */
function fromBinaryToHex(byte)
{
    result = byte.toString(16)

    if (result.length == 1) {
        result = "0" + result;
    }

    return result;
}

/**
 * 
 * @param {type} string String
 */
function fromStringToHex(string)
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

var filesToUpload;

/**
 * 
 * @param {type} files File[]
 * @param {type} currentIndex int
 */
function uploadFiles(files, currentIndex)
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

/**
 * 
 * @param {type} fileName String
 */
function removeFile(fileName)
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

/**
 * 
 * @param {type} folderName String
 */
function nextFolder(folderName)
{
    return $.post(
        {
            url: "nextFolder",
            headers: { "Folder-Name": fromStringToHex(folderName) },
            dataType: "text",
            success: function (data)
            {
                return data;
            }
        }
    );
}

function prevFolder()
{
    return $.post(
        {
            url: "prevFolder",
            dataType: "text",
            success: function (data)
            {
                return data;
            }
        }
    );
}

/**
 * 
 * @param {type} fileName String
 */
function downloadFile(fileName)
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

/**
 * 
 * @param {type} folderName String
 */
function createFolder(folderName)
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

var currentElementName;

/**
 * 
 * @param {type} elementName String
 */
function showPopup(elementName)
{
    currentElementName = elementName;
    itemPopupMenu.style.display = "flex";
    document.getElementById("create-folder-popup-menu").style.display = "none";
}

/**
 * 
 * @param {type} folderName String
 */
function nextFolderWrapper(folderName)
{
    nextFolder(folderName).then(() => window.location.href = "/storage");
}

/**
 * 
 * @param {type} folderName String
 */
function createFolderElement(folderName)
{
    if (folderName == "FAIL") {
        return;
    }

    return String.raw
        `<div class="listing__item" onclick="showPopup('${folderName}')" ondblclick="nextFolderWrapper('${folderName}')">
            <img src="/static/img/icons/folder.svg" alt="">
            <span>${folderName}</span>
        </div>`;
}

/**
 * 
 * @param {type} fileName String
 */
function createFileElement(fileName)
{
    if (fileName == "FAIL") {
        return;
    }

    return String.raw
        `<div class="listing__item" onclick="showPopup('${fileName}')">
            <img src="/static/img/icons/file.svg" alt="">
            <span>${fileName}</span>
        </div>`;
}

let downloadFileButton = document.querySelector('.popup-file__download');
let removeFileButton = document.querySelector('.popup-file__delete');
let itemPopupMenu = document.getElementById("item-popup-menu");
let createNewFolderButton = document.getElementById("create-new-folder");
let uploadButton = $("#upload-file");

uploadButton.change(takeFilesFromInput);

downloadFileButton.addEventListener("click", function ()
{
    itemPopupMenu.style.display = "none";

    downloadFile(currentElementName);

    window.location.href = "/storage";
})

removeFileButton.addEventListener("click", function ()
{
    itemPopupMenu.style.display = "none";

    removeFile(currentElementName);

    window.location.href = "/storage";
})

createNewFolderButton.addEventListener("click", function ()
{
    let folderName = $("#folder-name").val();

    if (folderName == "") {
        return;
    }

    createFolder(folderName).then(() => window.location.href = "/storage");
})

$("#create-folder").click(function ()
{
    itemPopupMenu.style.display = "none";

    document.getElementById("create-folder-popup-menu").style.display = "flex";
});

$("#previous-folder").click(function ()
{
    prevFolder().then(() => window.location.href = "/storage");
})

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