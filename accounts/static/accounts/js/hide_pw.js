// Login Page -> hide/show password button
function reveal() {
  if((document.getElementById('box').classList.contains('show-pw')) && document.getElementById('box').click){
    document.getElementById("pw").type="text";
    document.getElementById('box').classList.remove('show-pw')
  }
  else if(document.getElementById('box').click) {
    document.getElementById("pw").type='password';
    document.getElementById('box').classList.add('show-pw')
  }
}
