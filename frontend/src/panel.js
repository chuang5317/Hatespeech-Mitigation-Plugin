selectedText = window.getSelection().toString();
alert(selectedText);
var category = prompt("Which category of hatespeech does this belong to? Please enter either 'sexism', 'racism', or 'none':");
if (category == null || category == "") {
  category = "User cancelled the prompt.";
}
//do something to the window
//https://www.w3schools.com/jsref/met_win_open.asp
