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
