const registerButton = document.querySelector('#registration_form_submit')
registerButton.addEventListener('click', () => {
    registrationMessage = {
        username: document.querySelector('#registration_form_username').value,
        email: document.querySelector('#registration_form_email').value,
        password: document.querySelector('#registration_form_password').value,
        invitation_token: document.querySelector('#registration_form_invitation_token').value,
    }
    fetch('http://repo.cpmbits.com:8000/users', {
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
