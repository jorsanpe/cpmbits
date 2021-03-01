const registerButton = document.querySelector('#registration_form_submit');
const username = document.querySelector('#registration_form_username');
const email = document.querySelector('#registration_form_email');
const password = document.querySelector('#registration_form_password');
const repeatPassword = document.querySelector('#registration_form_repeat_password');


function displayFieldError(field, fieldStatus, errorMessage)
{
    fieldStatus.innerHTML = errorMessage;
    fieldStatus.className = "help is-danger";
    field.className = "input is-danger";
}


function displayFieldOk(field, fieldStatus)
{
    fieldStatus.innerHTML = "";
    fieldStatus.className = "help";
    field.className = "input is-success";
}


function validateField(field, fieldStatus, errorMessage)
{
    if (!field.checkValidity()) {
        displayFieldError(field, fieldStatus, errorMessage);
    } else {
        displayFieldOk(field, fieldStatus);
    }
}


email.addEventListener('input', function (event) {
    validateField(
        document.querySelector('#registration_form_email'),
        document.querySelector('#registration_form_email_status'),
        "email is invalid"
    );
});


username.addEventListener('input', function (event) {
    validateField(
        document.querySelector('#registration_form_username'),
        document.querySelector('#registration_form_username_status'),
        "username is invalid"
    );
});


function validateRepeatPassword()
{
    if (repeatPassword.value != password.value) {
        displayFieldError(
            repeatPassword, 
            document.querySelector('#registration_form_repeat_password_status'), 
            "passwords are not the same"
        );
    } else {
        displayFieldOk(
            repeatPassword, 
            document.querySelector('#registration_form_repeat_password_status')
        );
    }
}


password.addEventListener('input', function (event) {
    validateField(
        document.querySelector('#registration_form_password'),
        document.querySelector('#registration_form_password_status'),
        "password is invalid"
    );
    validateRepeatPassword();
});


repeatPassword.addEventListener('input', function (event) {
    validateRepeatPassword();
})


registerButton.addEventListener('click', () => {
    if (!username.checkValidity()
        || !email.checkValidity()
        || !password.checkValidity()
        || password.value != repeatPassword.value)
    {
        return;
    }

    var registrationMessage = {
        username: username.value,
        email: email.value,
        password: password.value,
    }
    fetch('https://repo.cpmbits.com:8000/users', {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(registrationMessage)
    })
    .then(response => {
        console.log(response.status)
        console.log(response.ok)
        if (response.status == 200) {
            window.location = "/registration_success.html";
        } else {
            window.location = "/registration_failure.html";
        }
    })
    .then(data => {});
})
