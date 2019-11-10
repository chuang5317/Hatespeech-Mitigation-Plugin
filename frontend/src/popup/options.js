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

document.getElementById("switch").onclick = function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.update(tabs[0].id, {url: tabs[0].url});
    });
};

document.addEventListener("DOMContentLoaded", restoreOptions);
