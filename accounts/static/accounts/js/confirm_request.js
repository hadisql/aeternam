// new connection request
$(document).ready(function() {

// the following function is triggered for both connection request and connection request cancel (undo the request)
const btnConfirmRequest = document.getElementById('confirm_request');
const btnToClick = document.getElementById('request_btn');

  if (btnConfirmRequest) {
    btnConfirmRequest.addEventListener('click', ()=> {
      btnToClick.click();
    });
  }

// the following function is triggered for the disconnect button (confirmation that user wants to disconnect their relation with another user)
const btnConfirmDisconnect = document.getElementById('confirm_disconnect');
const btnToClickToDisconnect = document.getElementById('disconnect_btn');

  if (btnConfirmDisconnect){
    btnConfirmDisconnect.addEventListener('click', ()=> {
      console.log("disconnect confirmation clicked")
      btnToClickToDisconnect.click();
    });
  }

})
