function restoreOptions() {
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
});

document.addEventListener("DOMContentLoaded", restoreOptions);


var reloadButton = document.getElementById("switch");
reloadButton.addEventListener("click", () => {
  console.log("Reload button clicked.");
  browser.tabs.reload();
});
