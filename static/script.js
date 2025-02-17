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

    errors.forEach(error => {
        const option = document.createElement('option');
        option.value = error.id;
        option.textContent = error.name;
        errorSelect.appendChild(option);
    });
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
                const imageContainer = document.getElementById('errorImages');
                imageContainer.innerHTML = '';
                
                // Display all images
                data.images.forEach(image => {
                    const img = document.createElement('img');
                    img.src = '/uploads/' + image;
                    img.alt = 'Изображение ошибки';
                    img.className = 'error-image img-thumbnail';
                    img.style.maxWidth = '200px';
                    imageContainer.appendChild(img);
                });

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
