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

        if (response.ok) {
            window.location.href = '/dashboard';
        } else {
        }
    } catch (error) {
        console.error('Error:', error);
    }
});