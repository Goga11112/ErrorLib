document.getElementById('createErrorForm').onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    await fetch('http://127.0.0.1:5000/api/errors', {
        method: 'POST',
        body: formData
    });
    fetchErrors();
};

async function fetchErrors() {
    const response = await fetch('http://127.0.0.1:5000/api/errors');
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
    img.style.maxWidth = '200px';

    const caption = document.createElement('div');
    caption.className = 'text-center mt-2';
    caption.textContent = `Рисунок ${index + 1}`;

    container.appendChild(img);
    container.appendChild(caption);
    return container;
}

document.getElementById('errorSelect').onchange = function() {
    const id = this.value;
    if (id) {
        fetch(`http://127.0.0.1:5000/api/errors/${id}`)
            .then(response => response.json())
            .then(data => {
                document.querySelector('input[name="errorId"]').value = id;
                document.getElementById('errorName').textContent = data.name;
                
                // Clear existing images
                const errorImagesContainer = document.getElementById('errorImages');
                errorImagesContainer.innerHTML = '';
                
                const solutionImagesContainer = document.getElementById('errorImagesRes');
                solutionImagesContainer.innerHTML = '';
                
                // Display error images
                if (data.error_images && Array.isArray(data.error_images)) {
                    data.error_images.forEach((image, index) => {
                        const imageElement = createImageElement(image, index, 'error');
                        errorImagesContainer.appendChild(imageElement);
                    });
                }
                
                // Display solution images
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
    await fetch(`http://127.0.0.1:5000/api/errors/${formData.get('errorId')}`, {
        method: 'PUT',
        body: formData
    });
    fetchErrors();
};

document.getElementById('deleteErrorButton').onclick = async () => {
    const errorId = document.querySelector('input[name="errorId"]').value;
    await fetch(`http://127.0.0.1:5000/api/errors/${errorId}`, {
        method: 'DELETE'
    });
    fetchErrors();
};

// Initial fetch of errors
fetchErrors();
