// notif delete from navbar
  // JavaScript to handle the click event
  document.querySelectorAll('.mark-as-read-icon').forEach(function (icon) {
    icon.addEventListener('click', function () {
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
            notifCard.classList.add('text-emerald-500', 'font-semibold');
            notifCard.querySelector('a').classList.add('hidden'); // Hide the anchor
            notifCard.querySelector('button').classList.add('hidden'); // Hide the button
            // Add new elements to the notification card
            const flexDiv = document.createElement('div');
            flexDiv.classList.add('flex-1');

            const markedAsSeen = document.createElement('p');
            markedAsSeen.textContent = 'Marked as seen';

            flexDiv.appendChild(markedAsSeen);
            notifCard.appendChild(flexDiv);
            // SVG CHECK ICON -------------
            const greenIconDiv = document.createElement('div');
            greenIconDiv.classList.add('text-emerald-500', 'font-semibold');

            const svgIcon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            svgIcon.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
            svgIcon.setAttribute('viewBox', '0 0 24 24');
            svgIcon.setAttribute('stroke-width', '1.5');
            svgIcon.classList.add('w-5', 'h-5', 'fill-none', 'stroke-current');

            const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            path.setAttribute('stroke-linecap', 'round');
            path.setAttribute('stroke-linejoin', 'round');
            path.setAttribute('d', 'M4.5 12.75l6 6 9-13.5');
            // -----------------------------
            svgIcon.appendChild(path);
            greenIconDiv.appendChild(svgIcon);
            notifCard.appendChild(greenIconDiv);

            var notifIndicator = document.getElementById('notif-indicator');
               if (notifIndicator) {
                   var notificationCount = parseInt(notifIndicator.innerHTML);
                   notifIndicator.innerHTML = (notificationCount - 1).toString();
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
