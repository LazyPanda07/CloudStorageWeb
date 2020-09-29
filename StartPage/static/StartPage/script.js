$.ajaxSetup({
    beforeSend: function (xhr, settings)
    {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
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

let registrationButton = document.querySelector('.header__reg-btn');
let authorizationButton = document.querySelector('.body__auth-btn');
let registrationButtonClose = document.querySelector('.reg-popup__close');
let authorizationButtonClose = document.querySelector('.auth-popup__close');
let registrationPopup = document.querySelector('.reg-popup');
let authorizationPopup = document.querySelector('.auth-popup');

registrationButton.addEventListener("click", function ()
{
    registrationPopup.style.display = "block";
    authorizationPopup.style.display = "none";
});

registrationButtonClose.addEventListener("click", function ()
{
    registrationPopup.style.display = "none";
});

authorizationButton.addEventListener("click", function ()
{
    authorizationPopup.style.display = "block";
    registrationPopup.style.display = "none";
});

authorizationButtonClose.addEventListener("click", function ()
{
    authorizationPopup.style.display = "none";
});

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