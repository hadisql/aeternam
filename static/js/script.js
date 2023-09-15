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
    const rotationAngleField = document.getElementById("rotation-angle");
    rotationAngleField.value = currentAngle;
}

// Photo Edit Page -> flip photo horizontally

function flipHorizontally() {
  const imgElement = document.getElementById("current_photo");
  imgElement.classList.toggle("transform");
  imgElement.classList.toggle("-scale-x-100");

  const imageFlipField = document.getElementById("mirror-flip"); //hidden django field
  imageFlipField.value = imageFlipField.value === 'True' ? 'False' : 'True'; // Toggle the value between 'True' and 'False'
}
document.getElementById("mirror_flip_btn").addEventListener("click", flipHorizontally);
