$(document).ready(function() {

  const albumId = document.getElementById('album_id').value; // used in the python back-end logic to update photos accordingly


  // Toggle button for AlbumAccess -> opens the modal window and preselect/deselects all photo thumbnail + message
  // const toggleButtons = document.querySelectorAll('#albumaccess-checkbox');
  // toggleButtons.forEach(toggleButton => {
  //   toggleButton.addEventListener('click', (event) => {
  //     const row = event.target.closest('tr'); // parent row element
  //     if(toggleButton.checked) {
  //       console.log('toggle button checked')
  //       var photoAccessButton = row.querySelector('#albumaccess-grant-button');
  //     } else {
  //       var photoAccessButton = row.querySelector('#albumaccess-revoke-button');
  //       console.log('toggle button unchecked')
  //     }
  //     if (photoAccessButton) {
  //       photoAccessButton.click(); // Trigger a click event on the button
  //     }
  //   })
  // })

  // Granting ALL access :
  document.querySelectorAll('#btn-grant-confirm').forEach( btnGrantConfirm => {
    btnGrantConfirm.addEventListener('click', () => {
      const relationToGrant = btnGrantConfirm.getAttribute('data-relation-id');
      const allPhotosSelection = [];
      // let's fill the list with all the photos :
      document.querySelectorAll(`input[data-checkbox-id="${relationToGrant}"]`).forEach(checkbox => {
        allPhotosSelection.push(checkbox.getAttribute('data-checkbox-photo-id'));
      })
      updatePhotoAccess(relationToGrant, allPhotosSelection, albumId);
    })
  });

  // Revoking ALL access :
  document.querySelectorAll('#btn-revoke-confirm').forEach( btnRevokeConfirm => {
    btnRevokeConfirm.addEventListener('click', () => {
      const relationToRevoke = btnRevokeConfirm.getAttribute('data-relation-id');
      const NoPhotosSelection = [];
      // we let the selection empty :
      updatePhotoAccess(relationToRevoke, NoPhotosSelection, albumId);
    })
  });

  // Let user choose (it opens the photo access modal)
  document.querySelectorAll(`button[id^=btn-let-me-choose_]`).forEach(btn => {
    btn.addEventListener('click', (event) => {
      const relationId = btn.getAttribute('id').replace('btn-let-me-choose_', ''); // parent row element
      const btnToClick = $(`#albumaccess_button_${relationId}`);
      btnToClick.click(); // opens the photo access modal
    })
  })

  // Display ring around clicked(and checked) photo thumbnails
  $('label[for^="checkbox_"]').click(function() {
    const checkboxId = $(this).attr('for');
    const checkbox = $(`#${checkboxId}`);
    if (checkbox.is(':checked')) {
      $(this).removeClass('ring-2 ring-offset-2 ring-current');
    } else {
      $(this).addClass('ring-2 ring-offset-2 ring-current');
    }
  });


  // MODAL WINDOW FOR EACH USER
  document.querySelectorAll('#continue-button').forEach( button => {
    button.addEventListener('click', () => {
      const relationId = button.getAttribute('data-relation-id');
      // console.log('relationId concerned :',relationId);
      const selectedPhotos = [];
      const checkboxes = document.querySelectorAll(`input[data-checkbox-id="${relationId}"]`);
      // console.log('checkboxes', checkboxes)
      checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
          selectedPhotos.push(checkbox.getAttribute('data-checkbox-photo-id'));
        }
      });
      // console.log(selectedPhotos);
      updatePhotoAccess(relationId, selectedPhotos, albumId);
    });
  });

  // function to fetch selected photos and trigger the python function
  function updatePhotoAccess(relationId, selectedPhotos, albumId) {
      fetch('/photo_access_manager/', {
        method: 'POST',
        body: JSON.stringify({
          relationId: relationId,
          selectedPhotos: selectedPhotos,
          albumId: albumId }),
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token
        },
      })
        .then((response) => {
          if (response.status === 200) {
            // console.log('success !! :', response.json());
            location.reload(); // refresh the page so the user sees the right informations
          } else {
            // console.log('error :',response.json());
          }
        })
        .catch((error) => {
          // Handle network error
        })
    }

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
