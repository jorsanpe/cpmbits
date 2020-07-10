const registerButton = document.querySelector('#registration_form_submit');
const username = document.querySelector('#registration_form_username');
const email = document.querySelector('#registration_form_email');
const password = document.querySelector('#registration_form_password');


function validateField(field, fieldStatus, errorMessage)
{
    if (!field.checkValidity()) {
        fieldStatus.innerHTML = errorMessage;
        fieldStatus.className = "help is-danger"
        field.className = "input is-danger"
    } else {
        fieldStatus.innerHTML = "";
        fieldStatus.className = "help"
        field.className = "input is-success"
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


password.addEventListener('input', function (event) {
    validateField(
        document.querySelector('#registration_form_password'),
        document.querySelector('#registration_form_password_status'),
        "password is invalid"
    );
});


registerButton.addEventListener('click', () => {
    if (!username.checkValidity() || !email.checkValidity() || !password.checkValidity()) {
        return;
    }

    var registrationMessage = {
        username: document.querySelector('#registration_form_username').value,
        email: email,
        password: password,
        invitation_token: document.querySelector('#registration_form_invitation_token').value,
    }
    fetch('http://localhost:8000/users', {
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
            window.location = "registration_success.html";
        } else {
            window.location = "registration_failure.html";
        }
    })
    .then(data => {});
})
