document.addEventListener('DOMContentLoaded', function () {
  const viewButton = document.getElementById('view-button');
  const swipeButton = document.getElementById('swipe-button');
  const galleryLayout = document.getElementById('photo-gallery-layout');
  const swipeLayout = document.getElementById('photo-swipe-layout');

  // Function to show the gallery layout and hide the swipe layout
  function showGalleryLayout() {
    console.log('show gallery');
    galleryLayout.classList.remove('hidden');
    swipeLayout.classList.add('hidden');

    // Swap the button classes
    viewButton.classList.remove('hover:text-accent-content');
    viewButton.classList.add('bg-base-300', 'shadow-sm');

    swipeButton.classList.remove('bg-base-300', 'shadow-sm');
    swipeButton.classList.add('hover:text-accent-content');
  }

  // Function to show the swipe layout and hide the gallery layout
  function showSwipeLayout() {
    console.log('show swipe');
    swipeLayout.classList.remove('hidden');
    galleryLayout.classList.add('hidden');

    // Swap the button classes
    swipeButton.classList.remove('hover:text-accent-content');
    swipeButton.classList.add('bg-base-300', 'shadow-sm');

    viewButton.classList.remove('bg-base-300', 'shadow-sm');
    viewButton.classList.add('hover:text-accent-content');
  }

  // Add click event listeners to the buttons
  viewButton.addEventListener('click', showGalleryLayout);
  swipeButton.addEventListener('click', showSwipeLayout);
});


// Login Page -> hide/show password button
function reveal() {
  if((document.getElementById('box').classList.contains('show-pw')) && document.getElementById('box').click){
    document.getElementById("pw").type="text";
    document.getElementById('box').classList.remove('show-pw')
  }
  else if(document.getElementById('box').click) {
    document.getElementById("pw").type='password';
    document.getElementById('box').classList.add('show-pw')
  }
}


// Photo Edit Page -> rotate photo
let currentAngle = 0;

function rotateImage(angle) {
    currentAngle += angle;
    const imgElement = document.getElementById("current_photo");
    imgElement.style.transform = `rotate(${currentAngle}deg)`;

    // Set the rotation angle in the hidden input field
    document.getElementById("rotation-angle").value = currentAngle;
}

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
