// Photo spinner when clicking 'save'
$(document).ready(function() {
  const saveBtn = document.getElementById('save_btn');
  const loadSpinner = document.getElementById('load_spinner');
  const fileInput = document.getElementById('fileInput');
  const fileInputLabel = document.getElementById('fileInputLabel');

    // Event listener for clicking on the save button
    saveBtn.addEventListener("click", (event) => {
      // Check if the file input has files selected
      if (fileInput.files.length > 0) {
        fileInput.classList.add('hidden');
        loadSpinner.classList.remove('hidden');
        if (fileInputLabel) {
          fileInputLabel.classList.add('hidden');
        }
        saveBtn.click();
        setTimeout(function() {
          saveBtn.disabled = true;  // Disable the "Save" button
        }, 300);
      } else {
        // Prevent the form submission if no files are selected
        console.log('No files selected');
        return;
      }
    });

    // Event listener for the form submit
    document.getElementById('addPhotoForm').addEventListener('submit', function() {
      console.log('Form submitted!');
    })
  });
