document.getElementById('createErrorForm').onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    await fetch('http://127.0.0.1:5000/api/errors', {  // Updated URL to match Flask server
        method: 'POST',
        body: formData
    });
    fetchErrors();
};

async function fetchErrors() {
    const response = await fetch('http://127.0.0.1:5000/api/errors');  // URL for fetching errors
    const errors = await response.json();
    const errorSelect = document.getElementById('errorSelect'); // Get the errorSelect element
    errorSelect.innerHTML = '<option value="">--Выберите ошибку--</option>'; // Reset select options

    errors.forEach(error => {
        const option = document.createElement('option'); // Create a new option element
        option.value = error.id; // Set the value to the error ID
        option.textContent = error.name; // Set the display text to the error name
        errorSelect.appendChild(option); // Add the option to the select element
    });
}

// Select error for updating
document.getElementById('errorSelect').onchange = function() {
    const id = this.value;
    if (id) {
        fetch(`http://127.0.0.1:5000/api/errors/${id}`)
            .then(response => response.json())
            .then(data => {
                document.querySelector('input[name="errorId"]').value = id;
                document.getElementById('errorName').textContent = data.name; // Display name in errorInfo
                document.getElementById('errorImage').src = data.image; // Display image in errorInfo
                document.getElementById('errorImage').style.display = 'block'; // Show image
                document.getElementById('errorSolution').textContent = data.solution; // Display solution in errorInfo

            });
    }
};

// Update error
document.getElementById('updateErrorForm').onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    await fetch(`http://127.0.0.1:5000/api/errors/${formData.get('errorId')}`, {
        method: 'PUT',
        body: formData
    });
    fetchErrors();
};

// Delete error
document.getElementById('deleteErrorButton').onclick = async () => {
    const errorId = document.querySelector('input[name="errorId"]').value;
    await fetch(`http://127.0.0.1:5000/api/errors/${errorId}`, {
        method: 'DELETE'
    });
    fetchErrors();
};

// Initial fetch of errors
fetchErrors();
