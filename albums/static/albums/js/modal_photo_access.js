$(document).ready(function() {

  const albumId = document.getElementById('album_id').value; // used in the python back-end logic to update photos accordingly
  const allPhotosList = document.getElementById('photo_list').value;

  // Granting ALL access :
  document.querySelectorAll('#btn-grant-confirm').forEach( btnGrantConfirm => {
    btnGrantConfirm.addEventListener('click', () => {
      const relationToGrant = btnGrantConfirm.getAttribute('data-relation-id');
      const allPhotosSelection = allPhotosList.split(',').map(num => parseInt(num.trim())).filter(num => !isNaN(num));
      updatePhotoAccess(relationToGrant, allPhotosSelection, albumId);
    });
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
      // const btnToClick = $(`#albumaccess_button_${relationId}`);
      const btnToClick = document.querySelector(`button#click-me-btn[data-relation-id="${relationId}"]`);
      btnToClick.click(); // opens the photo access modal
    })
  })

  // Display ring around clicked(and checked) photo thumbnails
  $('label[for^="checkbox_"]').click(function() {
    const checkboxId = $(this).attr('for');
    const checkbox = $(`#${checkboxId}`);
    if (checkbox.is(':checked')) {
      $(this).removeClass('ring-2 ring-offset-2 ring-current');
      $(this).addClass('blur-sm');
    } else {
      $(this).addClass('ring-2 ring-offset-2 ring-current');
      $(this).removeClass('blur-sm');
    }
  });

  // hidden button that trigger the unique modal with album photos
  const photoAccessBtn = document.getElementById('photoAccessBtn');
  // LOGIC TO TRIGGER THE MODAL WINDOW WITH CUSTOM PHOTO SELECTION
  document.querySelectorAll('#click-me-btn').forEach(button => {
    button.addEventListener('click', ()=> {
      const allowedPhotosList = [];
      const allowedPhotos = button.getAttribute('data-photolist');
      // save the allowed photos corresponding to the user in a list
      const photoNumbers = allowedPhotos.split(',').map(num => parseInt(num.trim())).filter(num => !isNaN(num));
      allowedPhotosList.push(...photoNumbers);
      console.log('allowed photos list :', allowedPhotosList);

      const relationToGrant = button.getAttribute('data-relation-id');
      console.log('relation :', relationToGrant)
      // set the relation id as an attribute in the save button of the unique modal
      document.getElementById('continue-button').setAttribute('data-relation-id', relationToGrant)

      // edit the modal window accordingly
      const inputBtn = document.querySelectorAll('input[id^="checkbox_"]').forEach(checkbox => {
        // set the relation id as an attribute in each checkbox (will be used when using the updatePhotoAccess function)
        checkbox.setAttribute('data-checkbox-id',relationToGrant)
        const photoId = checkbox.getAttribute('data-checkbox-photo-id');
        // save here the following label element in a const called labelToEdit
        const labelToEdit = checkbox.nextElementSibling;
        if (allowedPhotosList.includes(parseInt(photoId))) {
          console.log(photoId, 'in list');
          checkbox.checked = true;
          labelToEdit.classList.add("ring-2","ring-offset-2","ring-current");
          labelToEdit.classList.remove("blur-sm");
        } else {
          console.log(photoId, 'not in list');
          checkbox.checked = false;
          labelToEdit.classList.add("blur-sm");
          labelToEdit.classList.remove("ring-2","ring-offset-2","ring-current")
        }
      });
      photoAccessBtn.click();
    });
  });


  // SAME MODAL WINDOW FOR EACH USER
  document.querySelector('#continue-button').addEventListener('click', () => {
      const relationId = document.querySelector('#continue-button').getAttribute('data-relation-id');
      console.log('relation ID: ',relationId)
      // console.log('relationId concerned :',relationId);
      const selectedPhotos = [];
      const checkboxes = document.querySelectorAll(`input[data-checkbox-id="${relationId}"]`);
      // console.log('checkboxes', checkboxes)
      checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
          selectedPhotos.push(checkbox.getAttribute('data-checkbox-photo-id'));
        }
      });
      console.log('selected photos -> ' ,selectedPhotos);
      updatePhotoAccess(relationId, selectedPhotos, albumId);
    });


  // function to fetch selected photos and trigger the python function
  function updatePhotoAccess(relationId, selectedPhotos, albumId) {
    var baseUrlElement = document.getElementById('base-url');
    var baseUrl = baseUrlElement ? baseUrlElement.getAttribute('data-url') : '';

    if (!baseUrl) {
      console.error('Base URL not found');
      return;
    }
    var url = baseUrl;

    fetch(url, {
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
          console.log('success !! :', response.json());
          location.reload(); // refresh the page so the user sees the right informations
        } else {
          console.log('error :',response.json());
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
