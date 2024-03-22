document.getElementById("sign-out").addEventListener("click", async function() {
    try {
        const response = await fetch('/logout', {
            method: 'GET',
            credentials: "same-origin"
        });
        if (response.ok) {
            window.location.href = "/";
        } else {
            alert("Failed to log out");
        }
    } catch (error) {
        console.error('Error:', error);
    }
});