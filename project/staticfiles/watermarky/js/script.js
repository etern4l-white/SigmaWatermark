const fileUpload = document.getElementById('fileUpload');
const overlay = document.getElementById('fileUploadOverlay');

// Show overlay on drag enter
document.addEventListener('dragenter', (e) => {
    e.preventDefault();
    overlay.style.display = 'flex';  // Show the overlay
});

// Hide overlay when leaving the window
document.addEventListener('dragleave', (e) => {
    if (e.target === document || e.target === overlay) {
        overlay.style.display = 'none';  // Hide the overlay
    }
});

// Prevent default behavior for drag over
document.addEventListener('dragover', (e) => {
    e.preventDefault();
});

// Handle file drop event
document.addEventListener('drop', (e) => {
    e.preventDefault();
    overlay.style.display = 'none';  // Hide the overlay

    // Handle the dropped file
    if (e.dataTransfer && e.dataTransfer.files.length) {
        fileUpload.files = e.dataTransfer.files;  // Assign files to file input
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('uploadForm');
    const downloadSection = document.getElementById('downloadSection');
    const downloadLink = document.getElementById('downloadLink');
    const fileUpload = document.getElementById('fileUpload');
    const errorAlert = document.getElementById('errorAlert'); // Error alert

    form.addEventListener('submit', async function (e) {
        e.preventDefault();  // Prevent the default form submission

        const formData = new FormData(form);
        
        try {
            // Send the form data to the server via fetch
            const response = await fetch(form.getAttribute('action'), {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });

            if (response.ok) {
                const blob = await response.blob();  // Get the file from the response
                
                // Create a URL for the file and set it as the href for the download link
                const url = window.URL.createObjectURL(blob);
                downloadLink.href = url;

                // Set the download attribute to specify the filename
                const originalFileName = fileUpload.files[0].name;  // Get the original filename
                const baseName = originalFileName.split('.').slice(0, -1).join('.');  // Get base name
                const extension = originalFileName.split('.').pop();  // Get file extension
                downloadLink.download = `${baseName}_watermarked.${extension}`;  // Set the desired filename

                // Display the download section
                downloadSection.style.display = 'block';

                // Hide any previous error alerts
                errorAlert.style.display = 'none';
                downloadLink.disabled = false;

            } else {
                // Disable download link and show error alert
                downloadLink.disabled = true;
                downloadSection.style.display = 'none'; // Hide download section if error

                // Show Bootstrap alert
                errorAlert.innerHTML = 'File upload failed. Please try again.';
                errorAlert.style.display = 'block';
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            
            // Disable download link and show error alert
            downloadLink.disabled = true;
            downloadSection.style.display = 'none'; // Hide download section if error
            
            // Show Bootstrap alert with error message
            errorAlert.innerHTML = 'An error occurred while uploading the file. Please try again later.';
            errorAlert.style.display = 'block';
        }
    });
});

