function showAddUserForm() {
    document.getElementById('addUserForm').style.display = 'block';
}

document.getElementById('createUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('newUsername').value;
    const password = document.getElementById('newPassword').value;
    const isAdmin = document.getElementById('isAdmin').checked;

    const response = await fetch('/api/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password, is_admin: isAdmin })
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
