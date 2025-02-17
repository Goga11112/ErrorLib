document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

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
        // Добавляем или обновляем имя пользователя и кнопку регистрации в navbar
        const navbar = document.querySelector('.navbar-nav');
        
        // Удаляем старые элементы, если они существуют
        const oldUserElement = document.getElementById('userNavItem');
        if (oldUserElement) oldUserElement.remove();
        const oldRegisterButton = document.getElementById('registerNavItem');
        if (oldRegisterButton) oldRegisterButton.remove();

        // Добавляем кнопку регистрации
        const registerButton = document.createElement('li');
        registerButton.id = 'registerNavItem';
        registerButton.className = 'nav-item';
        registerButton.innerHTML = `<a class="nav-link" href="/register">Регистрация</a>`;
        navbar.appendChild(registerButton);

        // Добавляем имя пользователя (прижимаем вправо)
        const userElement = document.createElement('li');
        userElement.id = 'userNavItem';
        userElement.className = 'nav-item ms-auto'; // Добавляем ms-auto для выравнивания вправо
        userElement.innerHTML = `<span class="nav-user">${username}</span>`;
        navbar.appendChild(userElement);

       
    } else {
        messageDiv.textContent = result.message;
        messageDiv.className = 'alert alert-danger';
    }
});
