document.addEventListener('DOMContentLoaded', function() {
  // Get form and div elements
  var demoForm = document.getElementById('demoForm');
  var showAfterSubmission = document.getElementById('showAfterSubmission');
  var testBtn = document.getElementById('testBtn');

  // Add event listener to the form submission
  demoForm.addEventListener('submit', function(event) {
    // Add the 'hidden' class to the form
    demoForm.classList.add('hidden');
    // Remove the 'hidden' class from the div
    showAfterSubmission.classList.remove('hidden');

    // PROGRESS BAR
    var progressBarContainer = document.createElement("div");
        progressBarContainer.setAttribute("class", "relative w-full h-3 overflow-hidden rounded-full bg-neutral-100");

        // Create a new span element for the progress bar
        var progressBar = document.createElement("span");
        progressBar.setAttribute("class", "absolute w-24 h-full duration-300 ease-linear bg-neutral-900");
        progressBar.setAttribute("x-cloak", ""); // Optional, if using Alpine.js
        progressBar.style.width = "0%"; // Initial width

        // Append the progress bar to the container
        progressBarContainer.appendChild(progressBar);

        // Append the container to the target element
        document.getElementById("targetElement").appendChild(progressBarContainer);

        // Simulate progress animation
        var progress = 0;
        var progressInterval = setInterval(function() {
            progress += .75; //control the speed
            progressBar.style.width = progress + "%";
            if (progress >= 100) {
                clearInterval(progressInterval);
            }
        }, 100);
  });


  // demo form submission -> send form only when option selected
  function toggleSubmitButton() {
    var selectElement = document.getElementById("user_email");
    var submitButton = document.getElementById("submitBtn");

    if (selectElement.value === "") {
      submitButton.disabled = true;
    } else {
      submitButton.disabled = false;
    }
  }


});
