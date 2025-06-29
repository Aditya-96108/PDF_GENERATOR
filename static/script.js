// script.js: Handles frontend logic for Finlive Right AI PDF Generator
// Purpose: Sends a POST request to the FastAPI /api/v1/generate-pdf/ endpoint, manages the live loader
// with progress stages, and handles theme toggling. Optimized for a modern AI startup UI.
// Dependencies: None (uses native Fetch API).

function generatePDF() {
    const wordInput = document.getElementById('wordInput').value.trim();
    const pagesInput = document.getElementById('pagesInput').value;
    const companyInput = document.getElementById('companyInput').value.trim();
    const titleInput = document.getElementById('titleInput').value.trim();
    const authorInput = document.getElementById('authorInput').value.trim();
    const subjectInput = document.getElementById('subjectInput').value.trim();
    const errorElement = document.getElementById('error');
    const loaderElement = document.getElementById('loader');
    const loaderText = document.getElementById('loaderText');

    // Client-side validation
    if (!wordInput || wordInput.includes(' ')) {
        errorElement.textContent = 'Please enter a single keyword (e.g., Investment).';
        errorElement.style.display = 'block';
        return;
    }
    if (!pagesInput || pagesInput < 1 || pagesInput > 5) {
        errorElement.textContent = 'Please enter a valid number of pages (1-5).';
        errorElement.style.display = 'block';
        return;
    }
    if (!companyInput || !titleInput || !authorInput || !subjectInput) {
        errorElement.textContent = 'Please fill in all fields.';
        errorElement.style.display = 'block';
        return;
    }

    // Clear error and show loader
    errorElement.style.display = 'none';
    loaderElement.style.display = 'block';
    loaderText.textContent = 'Collecting Information...';

    // Make POST request to the API
    fetch('/api/v1/generate-pdf/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            word: wordInput,
            pages: parseInt(pagesInput),
            company: companyInput,
            title: titleInput,
            author: authorInput,
            subject: subjectInput
        })
    })
    .then(response => {
        loaderText.textContent = 'Generating PDF...';
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.detail || 'Failed to generate PDF. Please try again.');
            });
        }
        const filename = response.headers.get('content-disposition')
            ?.match(/filename="(.+)"/)?.[1] || `generated_${wordInput}.pdf`;
        return response.blob().then(blob => ({ blob, filename }));
    })
    .then(({ blob, filename }) => {
        loaderText.textContent = 'Downloading...';
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
        loaderText.textContent = 'Ready';
        setTimeout(() => {
            loaderElement.style.display = 'none';
        }, 1000);
    })
    .catch(error => {
        loaderElement.style.display = 'none';
        errorElement.textContent = `Error: ${error.message}`;
        errorElement.style.display = 'block';
        console.error('API request failed:', error);
    });
}

// Theme toggle functionality
document.getElementById('themeToggle').addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');
    const toggleBtn = document.getElementById('themeToggle');
    toggleBtn.textContent = document.body.classList.contains('dark-theme')
        ? '☀️ Light Mode'
        : '🌙 Dark Mode';
});