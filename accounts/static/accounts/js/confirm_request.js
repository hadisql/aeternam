// new connection request
$(document).ready(function() {

const btnConfirmRequest = document.getElementById('confirm_request');
const btnToClick = document.getElementById('request_btn');

  btnConfirmRequest.addEventListener('click', ()=> {
    btnToClick.click();
  });
})
