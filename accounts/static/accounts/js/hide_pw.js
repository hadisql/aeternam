// Login Page -> hide/show password button
function reveal() {
  if(document.getElementById('box').click){
    if(!document.getElementById('box').classList.contains('show-pw')) {
      document.getElementById("pw").type="text";
      document.getElementById('box').classList.add('show-pw');
      document.getElementById('pwHide').classList.add('hidden');
      document.getElementById('pwShow').classList.remove('hidden')
    }
    else {
      document.getElementById("pw").type='password';
      document.getElementById('box').classList.remove('show-pw');
      document.getElementById('pwHide').classList.remove('hidden');
      document.getElementById('pwShow').classList.add('hidden')
    }
  }
}
