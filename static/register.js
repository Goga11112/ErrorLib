document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
    });

    const result = await response.json();
    const messageDiv = document.getElementById('registerMessage');
    if (response.ok) {
        messageDiv.textContent = 'Регистрация успешна!';
        messageDiv.className = 'alert alert-success';
        setTimeout(() => window.location.href = '/login', 2000);
    } else {
        messageDiv.textContent = result.message;
        messageDiv.className = 'alert alert-danger';
    }
});
