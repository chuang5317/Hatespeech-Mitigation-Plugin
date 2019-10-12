function restoreOptions() {
  alert("here");
  function setCurrentChoice(item) {
    checkbox = document.querySelector('input[type="checkbox"]');
    checkbox.checked = item.HateSpeechOn;
  }
  function onError(error) {
    console.log(`Error: ${error}`);
  }
  var getting = browser.storage.sync.get("HateSpeechOn");
  getting.then(setCurrentChoice, onError);
}

var checkbox = document.querySelector('input[type="checkbox"]');
checkbox.addEventListener('change', function () {
  browser.storage.sync.set({
    HateSpeechOn : checkbox.checked
  });
  // function onError(error) {
  //   alert(`Error: ${error}`);
  // }
  //
  // function onGot(item) {
  //   alert(item.HateSpeechOn);
  // }
  // var getting = browser.storage.sync.get("HateSpeechOn");
  // getting.then(onGot, onError);
});
document.addEventListener("DOMContentLoaded", restoreOptions);
