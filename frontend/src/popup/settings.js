function restoreOptions() {
  function setCurrentChoice(item) {
    checkbox = document.getElementById("toggle-hover-effect");
    checkbox.checked = item.RevealOnHover;
  }
  function onError(error) {
    console.log(`Error: ${error}`);
  }
  var blurEffectSwitch = browser.storage.sync.get("RevealOnHover");
  blurEffectSwitch.then(setCurrentChoice, onError);
}

var checkbox = document.getElementById("toggle-hover-effect");
checkbox.addEventListener("change", function() {
  browser.storage.sync.set({
    RevealOnHover: checkbox.checked
  });
});

document.addEventListener("DOMContentLoaded", restoreOptions);
