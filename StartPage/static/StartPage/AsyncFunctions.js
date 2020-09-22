$.ajaxSetup({
    beforeSend: function (xhr, settings)
    {
        function getCookie(name)
        {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        }
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
                alert(data)
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