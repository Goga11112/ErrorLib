document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
            'Authorization': 'Basic ' + btoa(username + ':' + password)
        }
    });

    const result = await response.json();
    const messageDiv = document.getElementById('loginMessage');
    if (response.ok) {
        messageDiv.textContent = 'Авторизация успешна!';
        messageDiv.className = 'alert alert-success';
        // Закрываем аккордеон через 3 секунды
        setTimeout(() => {
            const authCollapse = new bootstrap.Collapse(document.getElementById('authCollapse'), {
                toggle: false
            });
            authCollapse.hide();
        }, 3000);
        // Показываем adminControls без перезагрузки страницы
        document.getElementById('adminControls').style.display = 'block';
    } else {
        messageDiv.textContent = result.message;
        messageDiv.className = 'alert alert-danger';
    }
});
