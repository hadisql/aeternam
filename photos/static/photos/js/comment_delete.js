// Photo detail page -> delete comment

$(document).ready(function() {
  // Function to handle button click and toggle visibility
  function showHideButtons(deleteButton, confirmButton) {
    deleteButton.classList.add("hidden");
    confirmButton.classList.remove("hidden");
  }

  // Attach event listeners to all button pairs
  const buttonPairs = document.querySelectorAll(".button-pair");
  buttonPairs.forEach((pair) => {
    const deleteButton = pair.querySelector(".delete-button");
    const confirmButton = pair.querySelector(".confirm-button");

    // Event listener for delete button
    deleteButton.addEventListener("click", (event) => {
      event.stopPropagation(); // Prevent bubbling up to document
      showHideButtons(deleteButton, confirmButton);
    });

    // Event listener for clicking anywhere else on the page
    document.addEventListener("click", () => {
      showHideButtons(confirmButton, deleteButton);
    });

    // Prevent clicking on the confirm button from hiding it immediately
    confirmButton.addEventListener("click", (event) => {
      event.stopPropagation();
    });
  });
});
