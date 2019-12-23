function restoreOptions() {
  function setCurrentChoice(item) {
    checkbox = document.getElementById("toggle-slider-input");
    checkbox.checked = item.HateSpeechOn;
  }
  function onError(error) {
    console.log(`Error: ${error}`);
  }
  var hatespeechSwitch = browser.storage.sync.get("HateSpeechOn");
  hatespeechSwitch.then(setCurrentChoice, onError);
}

function restoreFirstCustomCategory() {
  function setCurrentCategory(item) {
    firstCategory = document.getElementById("firstCategory");
    firstCategory.value = item.firstCustomSetting || '';
  }

  function onError(error) {
    console.log(`Error: ${error}`);
  }

  var firstCustomSetting = browser.storage.sync.get("firstCustomSetting");
  firstCustomSetting.then(setCurrentCategory, onError);
}

function restoreSecondCustomCategory() {
  function setCurrentCategory(item) {
    secondCategory = document.getElementById("secondCategory");
    secondCategory.value = item.secondCustomSetting || '';
  }

  function onError(error) {
    console.log(`Error: ${error}`);
  }

  var secondCustomSetting = browser.storage.sync.get("secondCustomSetting");
  secondCustomSetting.then(setCurrentCategory, onError);
}

var checkbox = document.getElementById("toggle-slider-input");
checkbox.addEventListener("change", function() {
  console.log(`Hatespeech detection set to ${checkbox.checked}.`);
  browser.storage.sync.set({
    HateSpeechOn: checkbox.checked
  });
  browser.tabs.reload();
});

var firstCategory = document.getElementById("firstCategory");
firstCategory.addEventListener("input", function() {
  browser.storage.sync.set({
    firstCustomSetting: firstCategory.value
  });
});

var secondCategory = document.getElementById("secondCategory");
secondCategory.addEventListener("input", function() {
  browser.storage.sync.set({
    secondCustomSetting: secondCategory.value
  });
});

document.addEventListener("DOMContentLoaded", restoreOptions);
document.addEventListener("DOMContentLoaded", restoreFirstCustomCategory);
document.addEventListener("DOMContentLoaded", restoreSecondCustomCategory);
