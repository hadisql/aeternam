// Photo detail page -> swipe left and right to show previous/next photos on mobile
// https://stackoverflow.com/questions/45648886/swipe-left-right-for-a-webpage?rq=3
var start = null;
var threshold = 100

 window.addEventListener("touchstart",function(event){
     console.log("touch");
   if(event.touches.length === 1){
      //just one finger touched
      start = event.touches.item(0).clientX;
    }else{
    start = null;
    }
  });

window.addEventListener("touchend",function(event){
    var offset = 100;//at least 100px are a swipe
    if(start){
        //document.body.innerHTML = " single touch end";
      //just one finger touched
      var end = event.changedTouches.item(0).clientX;

      // Calculate the horizontal swipe distance
      var distance = end - start;

      if(distance > threshold){
       // User swiped from left to right
       var leftArrowButton = document.getElementById("left_arrow");
       if (leftArrowButton) {
        leftArrowButton.click();
       }
      } else if (distance < -threshold) {
       // User swiped from right to left
       var rightArrowButton = document.getElementById("right_arrow");
       if (rightArrowButton) {
        rightArrowButton.click();
       }
      }
    }
  });
