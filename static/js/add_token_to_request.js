document.getElementById('sign-in').addEventListener('submit', async function(event) {
    event.preventDefault();
    const username = document.getElementById('inputUser').value;
    const password = document.getElementById('inputPassword').value;

    try {
        const response = await fetch('/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                username: username,
                password: password,
            }),
        });

        // Check for unsuccessful response (status code not ok)
        if (!response.ok) {
            alert('Login failed! Incorrect username or password.');
        } else {
            window.location.href = '/dashboard';
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
