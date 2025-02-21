const API_BASE_URL = 'http://localhost:5000';

document.getElementById('createErrorForm').onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const response = await fetch(`${API_BASE_URL}/api/errors`, {
        method: 'POST',
        body: formData
    });
    
    if (response.ok) {
        fetchErrors();
        clearForm();
    } else {
        const errorData = await response.json();
        showErrorMessage(errorData.message);
    }
};

function showErrorMessage(message) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

function clearForm() {
    document.getElementById('createErrorForm').reset();
    document.getElementById('errorMessage').style.display = 'none';
}

async function fetchErrors() {
    const response = await fetch(`${API_BASE_URL}/api/errors`);
    const errors = await response.json();
    const errorSelect = document.getElementById('errorSelect');
    errorSelect.innerHTML = '<option value="">--Выберите ошибку--</option>';

    if (errors && Array.isArray(errors)) {
        errors.forEach(error => {
            const option = document.createElement('option');
            option.value = error.id;
            option.textContent = error.name;
            errorSelect.appendChild(option);
        });
    }
}

function createImageElement(imageUrl, index, type) {
    const container = document.createElement('div');
    container.className = 'image-container mb-3';

    const img = document.createElement('img');
    img.src = '/uploads/' + imageUrl;
    img.alt = type === 'error' ? 'Изображение ошибки' : 'Изображение решения';
    img.className = 'error-image img-thumbnail';
    img.style.maxWidth = '200%';

    const caption = document.createElement('div');
    caption.className = 'text-center mt-2';
    caption.textContent = `Рисунок ${index + 1}`;

    container.appendChild(img);
    container.appendChild(caption);
    return container;
}

function setupSearch() {
    const searchInput = document.getElementById('searchError');
    const suggestions = document.getElementById('suggestions');
    let errors = {};

    fetch(`${API_BASE_URL}/api/errors`)
        .then(response => response.json())
        .then(data => {
            errors = data.reduce((acc, error) => {
                acc[error.id] = error;
                return acc;
            }, {});
        });

    searchInput.addEventListener('input', function() {
        const searchValue = this.value.toLowerCase();
        suggestions.innerHTML = '';

        if (searchValue) {
            const matchingErrors = Object.keys(errors).filter(key => 
                errors[key].name.toLowerCase().includes(searchValue)
            );

            if (matchingErrors.length > 0) {
                suggestions.style.display = 'block';
                matchingErrors.forEach(key => {
                    const suggestionItem = document.createElement('div');
                    suggestionItem.className = 'suggestion-item';
                    suggestionItem.textContent = errors[key].name;
                    suggestionItem.onclick = function() {
                        searchInput.value = errors[key].name;
                        suggestions.style.display = 'none';
                        document.getElementById('errorSelect').value = key;
                        document.getElementById('errorSelect').dispatchEvent(new Event('change'));
                    };
                    suggestions.appendChild(suggestionItem);
                });
            } else {
                suggestions.style.display = 'none';
            }
        } else {
            suggestions.style.display = 'none';
        }
    });

    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            const selectedError = Object.values(errors).find(error => 
                error.name.toLowerCase() === this.value.toLowerCase()
            );
            if (selectedError) {
                document.getElementById('errorSelect').value = selectedError.id;
                document.getElementById('errorSelect').dispatchEvent(new Event('change'));
            }
        }
    });
}

document.getElementById('errorSelect').onchange = function() {
    const id = this.value;
    if (id) {
        fetch(`${API_BASE_URL}/api/errors/${id}`)
            .then(response => response.json())
            .then(data => {
                document.querySelector('input[name="errorId"]').value = id;
                document.getElementById('errorName').textContent = data.name;
                
                const errorImagesContainer = document.getElementById('errorImages');
                errorImagesContainer.innerHTML = '';
                
                const solutionImagesContainer = document.getElementById('errorImagesRes');
                solutionImagesContainer.innerHTML = '';
                
                if (data.error_images && Array.isArray(data.error_images)) {
                    data.error_images.forEach((image, index) => {
                        const imageElement = createImageElement(image, index, 'error');
                        errorImagesContainer.appendChild(imageElement);
                    });
                }
                
                if (data.solution_images && Array.isArray(data.solution_images)) {
                    data.solution_images.forEach((image, index) => {
                        const imageElement = createImageElement(image, index, 'solution');
                        solutionImagesContainer.appendChild(imageElement);
                    });
                }

                document.getElementById('errorSolution').textContent = data.solution;
            });
    }
};

document.getElementById('updateErrorForm').onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const response = await fetch(`${API_BASE_URL}/api/errors/${formData.get('errorId')}`, {
        method: 'PUT',
        body: formData
    });
    
    if (response.ok) {
        fetchErrors();
    } else {
        const errorData = await response.json();
        showErrorMessage(errorData.message);
    }
};

document.getElementById('deleteErrorButton').onclick = async () => {
    const errorId = document.querySelector('input[name="errorId"]').value;
    await fetch(`${API_BASE_URL}/api/errors/${errorId}`, {
        method: 'DELETE'
    });
    fetchErrors();
};

    // Инициализация всех модальных окон
    document.addEventListener('DOMContentLoaded', function() {
        var modals = [].slice.call(document.querySelectorAll('.modal'));
        modals.forEach(function(modal) {
            new bootstrap.Modal(modal);
        });
    });
// Menu toggle functionality
document.getElementById('actionsBtn').addEventListener('click', () => {
    document.getElementById('actionsSection').style.display = 'block';
    document.getElementById('usersSection').style.display = 'none';
});

document.getElementById('usersBtn').addEventListener('click', () => {
    document.getElementById('actionsSection').style.display = 'none';
    document.getElementById('usersSection').style.display = 'block';
    fetchUsers();
});

async function fetchUsers() {
    const response = await fetch(`${API_BASE_URL}/api/users`);
    const users = await response.json();
    const usersList = document.getElementById('usersList');
    usersList.innerHTML = '';

    if (users && Array.isArray(users)) {
        users.forEach(user => {
            const userDiv = document.createElement('div');
            userDiv.className = 'user-item';
            userDiv.innerHTML = `
                <span>${user.username} (${user.is_admin ? 'Админ' : 'Пользователь'})</span>
                ${!user.is_admin ? `<button onclick="deleteUser(${user.id})">Удалить</button>` : ''}
            `;
            usersList.appendChild(userDiv);
        });
    }
}

async function deleteUser(userId) {
    if (confirm('Вы уверены, что хотите удалить этого пользователя?')) {
        const response = await fetch(`${API_BASE_URL}/api/users/${userId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            fetchUsers();
        } else {
            const errorData = await response.json();
            showErrorMessage(errorData.message);
        }
    }
}

// Initial setup
fetchErrors();
setupSearch();
