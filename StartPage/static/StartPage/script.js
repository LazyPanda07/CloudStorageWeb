$(document).ready(function ()
{
    $.ajaxSetup({
        beforeSend: function (xhr, settings)
        {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    /**
     * 
     * @param {type} login String
     * @param {type} password String
     */
    function authorization(login, password)
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

    /**
     * 
     * @param {type} login String
     * @param {type} password String
     */
    function registration(login, password)
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

    let registrationButton = $(".header__reg-btn")[0];
    let authorizationButton = $(".body__auth-btn")[0];
    let registrationButtonClose = $(".reg-popup__close")[0];
    let authorizationButtonClose = $(".auth-popup__close")[0];
    let registrationPopup = $(".reg-popup")[0];
    let authorizationPopup = $(".auth-popup")[0];

    registrationButton.addEventListener("click", (function ()
    {
        registrationPopup.style.display = "block";
        authorizationPopup.style.display = "none";
    }));

    registrationButtonClose.addEventListener("click", (function ()
    {
        registrationPopup.style.display = "none";
    }));

    authorizationButton.addEventListener("click", (function ()
    {
        authorizationPopup.style.display = "block";
        registrationPopup.style.display = "none";
    }));

    authorizationButtonClose.addEventListener("click", (function ()
    {
        authorizationPopup.style.display = "none";
    }));

    $("#log-in").click(function ()
    {
        authorization($("#authorization-login").val(), $("#authorization-password").val()).then(function (data)
        {
            if (data == "OK") {
                authorizationPopup.style.display = "none";

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

                    registrationPopup.style.display = "none";
                }
                else {
                    alert(data);
                }
            });
        }
    });
});