function restoreOptions() {
  function setCurrentChoice(item) {
    checkbox = document.getElementById("toggle-slider-input");
    checkbox.checked = item.HateSpeechOn;
  }
  function onError(error) {
    console.log(`Error: ${error}`);
  }
  var getting = browser.storage.sync.get("HateSpeechOn");
  getting.then(setCurrentChoice, onError);
}

var checkbox = document.getElementById("toggle-slider-input");
checkbox.addEventListener("change", function() {
  console.log(`Hatespeech detection set to ${checkbox.checked}.`);
  browser.storage.sync.set({
    HateSpeechOn: checkbox.checked
  });
});
document.addEventListener("DOMContentLoaded", restoreOptions);

var reloadButton = document.getElementById("reload-page-button");
reloadButton.addEventListener("click", () => {
  console.log("Reload button clicked.");
  browser.tabs.reload();
});
