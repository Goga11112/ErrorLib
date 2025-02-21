function showAddUserForm() {
    document.getElementById('addUserForm').style.display = 'block';
}

document.getElementById('createUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('newUsername').value;
    const password = document.getElementById('newPassword').value;
    const realname = document.getElementById('realUsername').value;
    const isAdmin = document.getElementById('isAdmin').checked;

    const response = await fetch('/api/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password,realname, is_admin: isAdmin })
    });

    const result = await response.json();
    const messageDiv = document.getElementById('createUserMessage');
    if (response.ok) {
        messageDiv.textContent = 'Пользователь успешно создан!';
        messageDiv.className = 'alert alert-success';
        setTimeout(() => window.location.reload(), 2000);
    } else {
        messageDiv.textContent = result.message;
        messageDiv.className = 'alert alert-danger';
    }
});

// Функция для удаления пользователя
async function deleteUser(userId) {
    if (confirm('Вы уверены, что хотите удалить этого пользователя?')) {
        try {
            const csrfMeta = document.querySelector('meta[name="csrf-token"]');
            if (!csrfMeta) {
                throw new Error('CSRF token meta tag not found');
            }

            const response = await fetch(`/api/users/${userId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfMeta.content
                }
            });


            
            const contentType = response.headers.get('content-type');
            if (response.ok) {
                loadUsers();
            } else if (contentType && contentType.includes('application/json')) {
                try {
                    const errorData = await response.json();
                    if (errorData.details) {
                        alert(`Ошибка: ${errorData.message}\n\nДетали:\n${JSON.stringify(errorData.details, null, 2)}`);
                    } else {
                    if (errorData.details && errorData.details.related_records_count) {
                        alert(`Невозможно удалить пользователя. Найдено ${errorData.details.related_records_count} связанных записей.`);
                    } else {
                        alert(errorData.message || 'Ошибка при удалении пользователя');
                    }

                    }
                } catch (jsonError) {
                    console.error('Ошибка парсинга JSON:', jsonError);
                    alert('Ошибка обработки ответа сервера');
                }
            } else {
                try {
                    const text = await response.text();
                    alert('Произошла ошибка: ' + text);
                } catch (textError) {
                    console.error('Ошибка чтения текста ответа:', textError);
                    alert('Не удалось прочитать ответ сервера');
                }
            }

        } catch (error) {
            console.error('Ошибка при удалении пользователя:', error);
            if (error.message === 'CSRF token meta tag not found') {
                alert('Ошибка безопасности: CSRF токен не найден. Пожалуйста, перезагрузите страницу.');
            } else {
                alert('Произошла непредвиденная ошибка при удалении пользователя');
            }

        }
    }
}


// Загрузка списка пользователей при открытии страницы
async function loadUsers() {

    const response = await fetch('/api/users');
    const users = await response.json();
    const usersList = document.getElementById('usersList');
    
    usersList.innerHTML = users.map(user => `
        <tr>
            <td>${user.username}</td>
            <td>${user.is_admin ? 'Администратор' : 'Пользователь'}</td>
            <td>
                <button class="btn btn-danger btn-sm" onclick="deleteUser(${user.id})">Удалить</button>
            </td>
        </tr>
    `).join('');
}

// Инициализация при загрузке страницы
window.onload = () => {
    loadUsers();
};
