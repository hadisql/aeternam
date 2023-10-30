document.addEventListener('DOMContentLoaded', function () {
  const viewButton = document.getElementById('view-button');
  const viewSmallerButton = document.getElementById('view-smaller-button');
  const swipeButton = document.getElementById('swipe-button');
  const galleryLayout = document.getElementById('photo-gallery-layout');
  const swipeLayout = document.getElementById('photo-swipe-layout');


  // Function to show the gallery with smaller photos and hide the swipe layout if necessary
  function showSmallerGalleryLayout() {
    var isSwipeShown = !swipeLayout.classList.contains('hidden');
    var isGalleryBig = galleryLayout.classList.contains('grid-cols-2');

    console.log('show smaller gallery');

    if (isSwipeShown) {
      // SWIPE -> SMALL GALLERY
      console.log('swipe -> small gallery');
      if (isGalleryBig) {
        // if the last state of galleryLayout was the 'big' gallery
        galleryLayout.classList.remove('grid-cols-2','lg:grid-cols-3','xl:grid-cols-4','gap-x-6', 'gap-y-10');
        galleryLayout.classList.add('grid-cols-3', 'lg:grid-cols-4', 'xl:grid-cols-5','gap-x-4', 'gap-y-6');
      }
      swipeLayout.classList.add('hidden');
      galleryLayout.classList.remove('hidden');
      swipeButton.classList.remove('bg-base-300', 'shadow-sm');
      swipeButton.classList.add('hover:text-accent-content');
    } else {
      // GALLERY -> SMALL GALLERY
      if (isGalleryBig) {
        console.log('gallery -> small gallery');
        // if the last state of galleryLayout was the 'big' gallery // else is the case of clicking on small gallery while it's already showing
        galleryLayout.classList.remove('grid-cols-2','lg:grid-cols-3','xl:grid-cols-4','gap-x-6', 'gap-y-10');
        galleryLayout.classList.add('grid-cols-3', 'lg:grid-cols-4', 'xl:grid-cols-5','gap-x-4', 'gap-y-6');
        viewButton.classList.remove('bg-base-300', 'shadow-sm');
        viewButton.classList.add('hover:text-accent-content');
      }
    }
    // Swap the button classes
    viewSmallerButton.classList.remove('hover:text-accent-content');
    viewSmallerButton.classList.add('bg-base-300', 'shadow-sm');

  }

  // Function to show the gallery layout and hide the swipe layout
  function showGalleryLayout() {
    console.log('show big gallery');
    var isSwipeShown = !swipeLayout.classList.contains('hidden');
    var isGalleryBig = galleryLayout.classList.contains('grid-cols-2');

    if (isSwipeShown) {
      // SWIPE -> GALLERY
      // when clicking on the middle button, if the swipe was not hidden <=> passing from swipe to gallery
      if (isGalleryBig) {
        console.log('swipe -> big gallery');
        // if the last state of galleryLayout was the 'big' gallery
        galleryLayout.classList.remove('hidden');
        swipeLayout.classList.add('hidden');
      } else {
        // if the last state of galleryLayout was the 'small' gallery
        galleryLayout.classList.remove('hidden','grid-cols-3', 'lg:grid-cols-4', 'xl:grid-cols-5','gap-x-4', 'gap-y-6');
        galleryLayout.classList.add('grid-cols-2','lg:grid-cols-3','xl:grid-cols-4','gap-x-6', 'gap-y-10');
      }

      swipeButton.classList.remove('bg-base-300', 'shadow-sm');
      swipeButton.classList.add('hover:text-accent-content');
    } else {
      // SMALL GALLERY -> GALLERY
      if (!isGalleryBig) {
        console.log('small gallery -> big gallery');
        // if the last state of galleryLayout was the 'big' gallery // else is the case of clicking on small gallery while it's already showing
        galleryLayout.classList.add('grid-cols-2','lg:grid-cols-3','xl:grid-cols-4','gap-x-6', 'gap-y-10');
        galleryLayout.classList.remove('grid-cols-3', 'lg:grid-cols-4', 'xl:grid-cols-5','gap-x-4', 'gap-y-6');
        viewSmallerButton.classList.remove('bg-base-300', 'shadow-sm');
        viewSmallerButton.classList.add('hover:text-accent-content');
      }
    }
    // Swap the button classes
    viewButton.classList.remove('hover:text-accent-content');
    viewButton.classList.add('bg-base-300', 'shadow-sm');
  }

  // Function to show the swipe layout and hide the gallery layout
  function showSwipeLayout() {
    console.log('show swipe');
    var isSwipeShown = !swipeLayout.classList.contains('hidden');
    if (!isSwipeShown) {
      // the else condition is clicking while already showing swipe

      swipeLayout.classList.remove('hidden');
      galleryLayout.classList.add('hidden');

      swipeButton.classList.remove('hover:text-accent-content');
      swipeButton.classList.add('bg-base-300', 'shadow-sm');

      if (viewButton.classList.contains('bg-base-300')) {
        // From gallery layout to Swap layout
        viewButton.classList.remove('bg-base-300', 'shadow-sm');
        viewButton.classList.add('hover:text-accent-content');
      } else if (viewSmallerButton.classList.contains('bg-base-300')) {
        // From smaller gallery layout to Swap layout
        viewSmallerButton.classList.remove('bg-base-300', 'shadow-sm');
        viewSmallerButton.classList.add('hover:text-accent-content');
      }
    }

  }

  // Add click event listeners to the buttons
  viewButton.addEventListener('click', showGalleryLayout);
  swipeButton.addEventListener('click', showSwipeLayout);
  viewSmallerButton.addEventListener('click', showSmallerGalleryLayout);
});
