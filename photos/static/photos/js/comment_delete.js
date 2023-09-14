// Photo detail page -> delete comment

// Function to handle button click and toggle visibility
function del_comment(deleteButton, confirmButton) {
  deleteButton.classList.add("hidden");
  confirmButton.classList.remove("hidden");
}

// // Attach event listeners to all button pairs
// const buttonPairs = document.querySelectorAll(".button-pair");
// buttonPairs.forEach((pair) => {
//   const deleteButton = pair.querySelector(".delete-button");
//   const confirmButton = pair.querySelector(".confirm-button");

//   deleteButton.addEventListener("click", () => del_comment(deleteButton, confirmButton));
// });

// Function to show delete button and hide confirm button
function showDeleteButton(deleteButton, confirmButton) {
  deleteButton.classList.remove("hidden");
  confirmButton.classList.add("hidden");
}

// Attach event listeners to all button pairs
const buttonPairs = document.querySelectorAll(".button-pair");
buttonPairs.forEach((pair) => {
  const deleteButton = pair.querySelector(".delete-button");
  const confirmButton = pair.querySelector(".confirm-button");

  // Event listener for delete button
  deleteButton.addEventListener("click", (event) => {
    event.stopPropagation(); // Prevent bubbling up to document
    del_comment(deleteButton, confirmButton);
  });

  // Event listener for clicking anywhere else on the page
  document.addEventListener("click", () => {
    showDeleteButton(deleteButton, confirmButton);
  });

  // Prevent clicking on the confirm button from hiding it immediately
  confirmButton.addEventListener("click", (event) => {
    event.stopPropagation();
  });
});
