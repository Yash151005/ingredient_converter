document.addEventListener('DOMContentLoaded', function () {
    // Mobile Navigation Toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle) {
        menuToggle.addEventListener('click', function () {
            navLinks.classList.toggle('active');
        });
    }

    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-messages .message');
    flashMessages.forEach(function (message) {
        setTimeout(function () {
            message.style.opacity = '0';
            message.style.transition = 'opacity 1s';
            setTimeout(function () {
                message.remove();
            }, 1000);
        }, 5000);
    });

    // Password match validation for signup
    const signupForm = document.querySelector('.auth-form');
    if (signupForm && signupForm.getAttribute('action').includes('signup')) {
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirm_password');

        function validatePassword() {
            if (password.value !== confirmPassword.value) {
                confirmPassword.setCustomValidity("Passwords don't match");
            } else {
                confirmPassword.setCustomValidity('');
            }
        }

        if (password && confirmPassword) {
            password.addEventListener('change', validatePassword);
            confirmPassword.addEventListener('keyup', validatePassword);
        }
    }

    // ✅ Ingredient Conversion Form Submission
    const convertForm = document.getElementById('convert-form');
    if (convertForm) {
        convertForm.addEventListener('submit', function (e) {
            e.preventDefault(); // Prevent default form submission

            const ingredient = document.getElementById('ingredient').value;
            const amount = document.getElementById('amount').value;
            const unit = document.getElementById('unit').value;

            fetch('/ml/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ ingredient, amount, unit }),
            })
                .then(response => response.json())
                .then(data => {
                    const resultBox = document.getElementById('conversion-result');
                    if (data.converted_grams) {
                        resultBox.textContent = `${amount} ${unit} of ${ingredient} is approximately ${data.converted_grams} grams.`;
                    } else if (data.error) {
                        resultBox.textContent = `Error: ${data.error}`;
                    } else {
                        resultBox.textContent = 'Conversion failed. Please try again.';
                    }
                })
                .catch(error => {
                    console.error('Conversion error:', error);
                    const resultBox = document.getElementById('conversion-result');
                    resultBox.textContent = 'An error occurred while converting.';
                });
        });
    }
});
