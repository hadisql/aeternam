// profile page update

const profilePic = document.getElementById("profile_pic")
const clearButton = document.getElementById("clear_label_btn")
const clearText = document.getElementById("clear_text")

function blurProfilePic() {
  if (document.getElementById("profile_picture-clear_id").checked) {
    profilePic.style.opacity = 0.3
    clearText.innerHTML = 'Unclear'
    clearButton.classList.add("btn-primary")
  } else {
    profilePic.style.opacity = 1
    clearText.innerHTML = 'Clear'
    clearButton.classList.remove("btn-primary")
  }
}
document.getElementById('profile_picture-clear_id').addEventListener("click", blurProfilePic);
