// Function to switch delete icon for notifications (2 clicks to delete)
function showDeleteButton(deleteButton, confirmButton) {
  deleteButton.classList.add("hidden");
  confirmButton.classList.remove("hidden");
}

$(document).ready(function() {
  // Attach event listeners to all button pairs
  const buttonPairs = document.querySelectorAll(".delete-notif-pair");
  buttonPairs.forEach((pair) => {
    const deleteButton = pair.querySelector(".delete-notif");
    const confirmButton = pair.querySelector(".confirm-delete-notif");

    // Event listener for delete button
    deleteButton.addEventListener("click", (event) => {
      event.stopPropagation(); // Prevent bubbling up to document
      showDeleteButton(deleteButton, confirmButton);
    });

    // Event listener for clicking anywhere else on the page
    document.addEventListener("click", () => {
      showDeleteButton(confirmButton, deleteButton);
    });

    // Prevent clicking on the confirm button from hiding it immediately
    confirmButton.addEventListener("click", (event) => {
      event.stopPropagation();
    });
  });

  // notif delete from navbar
  // JavaScript to handle the click event
  document.querySelectorAll('.confirm-delete-notif').forEach(function (icon) {
    icon.addEventListener('click', function () {
        var notificationId = this.closest('#notif').getAttribute('data-notification-id');
        markNotificationAsRead(notificationId);
    });
  });
  // mark notification as read when link is clicked
  document.querySelectorAll('.mark-as-read-link').forEach(function (link) {
    link.addEventListener('click', function () {
        var notificationId = this.closest('#notif').getAttribute('data-notification-id');
        markNotificationAsRead(notificationId);
    });
  });

  function markNotificationAsRead(notificationId) {
    // Send an AJAX request to mark the notification as read
    fetch(`/clear_notif_from_navbar/${notificationId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token
            'X-Requested-With': 'XMLHttpRequest', // To identify AJAX requests in Django
        },
    })
    .then(function (response) {
        if (response.status === 200) {
            // Update the UI to indicate that the notification is read (e.g., change the icon color)
            const notifCard = document.querySelector(`[data-notification-id="${notificationId}"]`);
            notifCard.classList.add('notification-fade-out');
            notifCard.addEventListener('transitionend', function() {
              notifCard.remove();
          });

          var notifIndicator = document.getElementById('notif-indicator');
          if (notifIndicator) {
              var notificationCount = parseInt(notifIndicator.innerHTML);
              notifIndicator.innerHTML = (notificationCount - 1).toString();
              if (parseInt(notifIndicator.innerHTML) == 0) {
                  // Remove the span with class 'indicator-item'
                  var indicatorItem = document.querySelector('.indicator-item');
                  if (indicatorItem) {
                      indicatorItem.remove();
                  }
              }
          }
        }
    });
  }

  // Function to get the CSRF token from cookies
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = cookies[i].trim();
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
});
