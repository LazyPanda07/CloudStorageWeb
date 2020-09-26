$.ajaxSetup({
    beforeSend: function (xhr, settings)
    {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});

function toHex(/** uint8 */ byte)
{
    result = byte.toString(16)

    if (result.length == 1) {
        result = "0" + result;
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
                alert(data)
            }
        }
    );
}

function uploadFile(/** File */ file)
{
    let reader = new FileReader();

    reader.readAsArrayBuffer(file);

    reader.addEventListener("load", (event) =>
    {
        let data = new Uint8Array(event.target.result);
        let binaryString = "";

        for (const i of data) {
            binaryString += toHex(i);
        }

        return $.post(
            {
                url: "/uploadFile",
                headers: { "File-Name": file.name },
                data: binaryString,
                success: function (data)
                {
                    alert(data);
                }
            }
        );
    });
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
            url: "/getFiles",
            dataType: "text",
            success: function (data)
            {
                alert(data);
            }
        }
    );
}

function removeFile(/** String */ fileName)
{
    return $.post(
        {
            url: "/removeFile",
            headers: { "File-Name": fileName },
            dataType: "text",
            success: function (data)
            {
                alert(data);
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
            url: "/setFileName",
            dataType: "text",
            headers: { "File-Name": fileName },
            success: function (data)
            {
                console.log(data);
            }
        }
    ).then(() =>
    {
        window.location = "/downloadFile";
    });
}

function createFolder(/** String */ folderName)
{
    $.post(
        {
            url: "/createFolder",
            dataType: "text",
            headers: { "Folder-Name": folderName },
            success: function (data)
            {
                console.log(data);
            }
        }
    )
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

regBtn.addEventListener("click", function ()
{
    regPopup.style.display = "block";
    authPopup.style.display = "none";
});

regBtnClose.addEventListener("click", function ()
{
    regPopup.style.display = "none";
});

authBtn.addEventListener("click", function ()
{
    authPopup.style.display = "block";
    regPopup.style.display = "none";
});

authBtnClose.addEventListener("click", function ()
{
    authPopup.style.display = "none";
});

$("#logIn").click(function ()
{
    authorization($("#authorizationLogin").val(), $("#authorizationPassword").val()).then(function (data)
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