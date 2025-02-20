// Get currentUser from container data attribute
const container = document.querySelector('.container');
const currentUser = {
    is_admin: false
};

async function checkAuth() {
    try {
        const response = await fetch('/api/check-auth', {
            method: 'GET',
            credentials: 'include'
        });

        if (response.ok) {
            const data = await response.json();
            if (data.authenticated) {
                currentUser.is_admin = data.is_admin || false;
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

document.addEventListener('DOMContentLoaded', function() {
    // Wait for Bootstrap to be fully loaded
    if (typeof bootstrap === 'undefined') {
        console.error('Bootstrap is not loaded!');
        return;
    }
    
    // Initialize Bootstrap modals
    var modals = [].slice.call(document.querySelectorAll('.modal'));
    modals.forEach(function(modal) {
        new bootstrap.Modal(modal);
    });

    checkAuth(); // Check authentication on page load
    loadTopics();

    // Обработка добавления новой темы
    document.getElementById('addTopicForm').addEventListener('submit', async (e) => {
        console.log('Form submission started');
        e.preventDefault();
        
        try {
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());
            console.log('Form data:', data);

            const response = await fetch('/api/error-topics', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            console.log('API response status:', response.status);
            
            if (response.ok) {
                const result = await response.json();
                console.log('Topic created successfully:', result);
                $('#addTopicModal').modal('hide');
                e.target.reset();
                loadTopics();
            } else {
                const error = await response.json();
                console.error('Error creating topic:', error);
                alert(`Ошибка при добавлении темы: ${error.message || 'Неизвестная ошибка'}`);
            }
        } catch (error) {
            console.error('Error during form submission:', error);
            alert('Произошла ошибка при отправке формы. Проверьте консоль для подробностей.');
        }
    });

    // Обработка редактирования темы
    document.getElementById('editTopicForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        try {
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());
            const topicId = data.id;

            const response = await fetch(`/api/error-topics/${topicId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                const result = await response.json();
                console.log('Topic updated successfully:', result);
                $('#editTopicModal').modal('hide');
                loadTopics();
            } else {
                const error = await response.json();
                console.error('Error updating topic:', error);
                alert(`Ошибка при обновлении темы: ${error.message || 'Неизвестная ошибка'}`);
            }
        } catch (error) {
            console.error('Error during form submission:', error);
            alert('Произошла ошибка при отправке формы. Проверьте консоль для подробностей.');
        }
    });
});

async function loadTopics() {
    const response = await fetch('/api/error-topics');
    const topics = await response.json();
    const tableBody = document.getElementById('topicsTable');
    tableBody.innerHTML = '';

    topics.forEach(topic => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${topic.topic}</td>
            <td>${topic.responsible}</td>
            <td>${topic.phone}</td>
            ${currentUser.is_admin ? `
            <td>
                <button class="btn btn-sm btn-warning me-2" onclick="editTopic(${topic.id})">Изменить</button>
                <button class="btn btn-sm btn-danger" onclick="deleteTopic(${topic.id})">Удалить</button>
            </td>
            ` : ''}
        `;

        tableBody.appendChild(row);
    });
}

async function editTopic(id) {
    try {
        const response = await fetch(`/api/error-topics/${id}`);
        if (response.ok) {
            const topic = await response.json();
            document.getElementById('editTopicId').value = topic.id;
            document.getElementById('editTopic').value = topic.topic;
            document.getElementById('editResponsible').value = topic.responsible;
            document.getElementById('editPhone').value = topic.phone;
            
            const editModal = new bootstrap.Modal(document.getElementById('editTopicModal'));
            editModal.show();
        } else {
            const error = await response.json();
            console.error('Error fetching topic:', error);
            alert(`Ошибка при получении темы: ${error.message || 'Неизвестная ошибка'}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Произошла ошибка. Проверьте консоль для подробностей.');
    }
}

async function deleteTopic(id) {
    if (confirm('Вы уверены, что хотите удалить эту тему?')) {
        const response = await fetch(`/api/error-topics/${id}`, {
            method: 'DELETE' 
        });

        if (response.ok) {
            loadTopics();
        } else {
            alert('Ошибка при удалении темы');
        }
    }
}
