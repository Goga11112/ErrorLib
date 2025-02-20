// Проверка авторизации при загрузке страницы
async function checkAuth() {
    try {
        const response = await fetch('/api/check-auth', {
            method: 'GET',
            credentials: 'include'
        });

        if (response.ok) {
            const data = await response.json();
            if (data.authenticated) {
                document.querySelectorAll('.auth-only').forEach(el => el.style.display = 'block');
                document.querySelectorAll('.login-only').forEach(el => el.style.display = 'none');
            }
        } else {
            console.error('Ошибка при проверке авторизации:', response.statusText);
        }
    } catch (error) {
        console.error('Ошибка сети:', error);
    }
}

// Проверяем авторизацию при загрузке страницы
checkAuth();

const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        e.stopPropagation(); // Prevent event bubbling
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        // Get the original destination from form or default to '/'
        const nextInput = document.querySelector('input[name="next"]');
        const nextUrl = nextInput ? nextInput.value : '/';
        console.log('Next URL:', nextUrl); // Debug logging

        // Disable submit button to prevent multiple submissions
        const submitBtn = document.querySelector('.login-btn');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Вход...';

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Authorization': 'Basic ' + btoa(username + ':' + password),
                    'Content-Type': 'application/json'
                }
            });

            const result = await response.json();
            const messageDiv = document.getElementById('loginMessage');
            if (response.ok) {
                messageDiv.textContent = 'Авторизация успешна!';
                messageDiv.className = 'alert alert-success';

                // Update UI elements
                document.querySelectorAll('.auth-only').forEach(el => el.style.display = 'block');
                document.querySelectorAll('.login-only').forEach(el => el.style.display = 'none');
                
                // Update URL without refreshing
                window.history.pushState({}, '', nextUrl);
                checkAuth(); // Refresh auth state
            } else {
                messageDiv.textContent = result.message;
                messageDiv.className = 'alert alert-danger';
                // Re-enable submit button on error
                submitBtn.disabled = false;
                submitBtn.textContent = 'Войти';
            }
        } catch (error) {
            console.error('Ошибка сети:', error);
        }
    });
} else {
    console.error('Элемент loginForm не найден');
}
