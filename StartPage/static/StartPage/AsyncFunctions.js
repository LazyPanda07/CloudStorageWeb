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
            binaryString += String.fromCharCode(i);
        }

        return $.post(
            {
                url: "/uploadFile",
                dataType: "text",
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