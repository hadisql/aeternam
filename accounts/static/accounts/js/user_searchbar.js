const userInput = $('#user-input')
const searchIcon = $('#search-icon')
const resultsDiv = $('#replaceable-content')
const endpoint = '/user-search/'
const delay_by_in_ms = 700
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
  $.getJSON(endpoint, request_parameters)
      .done(response => {
          console.log(response);
          // fade out the resultsDiv, then:
          resultsDiv.fadeTo('fast', 0).promise().then(() => {
              // replace the HTML contents
              resultsDiv.html(response['html_from_view'])
              // fade-in the div with new contents
              resultsDiv.fadeTo('fast', 1)
              // stop animating search icon
              searchIcon.removeClass('blink')
          })
      })
}

userInput.on('keyup', function () {

  const request_parameters = {
      q: $(this).val() // value of userInput: the HTML element with ID user-input
  }

  // start animating the search icon with the CSS class
  searchIcon.addClass('blink')

  // if scheduled_function is NOT false, cancel the execution of the function
  if (scheduled_function) {
      clearTimeout(scheduled_function)
  }

  // setTimeout returns the ID of the function to be executed
  scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})
