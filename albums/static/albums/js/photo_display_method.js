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
