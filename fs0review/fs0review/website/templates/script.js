// script.js
document.addEventListener('DOMContentLoaded', function() {
    var registerButton = document.getElementById('registerButton');
    registerButton.addEventListener('click', validateInputs);
});

function validateInputs() {
    var nameInput = document.getElementById('nameInput');
    var emailInput = document.getElementById('emailInput');
    var passwordInput = document.getElementById('passwordInput');

    var name = nameInput.value.trim();
    var email = emailInput.value.trim();
    var password = passwordInput.value.trim();

    if (name === '') {
        alert('Please enter your name.');
        nameInput.focus();
        return;
    }

    if (email === '') {
        alert('Please enter your email.');
        emailInput.focus();
        return;
    }

    if (password === '') {
        alert('Please enter your password.');
        passwordInput.focus();
        return;
    }

    // Perform additional validation checks as needed

    // If all inputs are valid, proceed with registration process
    alert('Registration successful!');

    // Clear the input fields
    nameInput.value = '';
    emailInput.value = '';
    passwordInput.value = '';
}