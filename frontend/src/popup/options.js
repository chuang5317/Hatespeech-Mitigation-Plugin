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

function restoreRacismCategory() {
  function setCurrentChoice(item) {
    racism = document.getElementById("racism");
    racism.checked = item.RacismFiltered;
  }
  function onError(error) {
    console.log(`Error: ${error}`);
  }
  var racismCheckbox = browser.storage.sync.get("RacismFiltered");
  racismCheckbox.then(setCurrentChoice, onError);
}

function restoreSexismCategory() {
  function setCurrentChoice(item) {
    sexism = document.getElementById("sexism");
    sexism.checked = item.SexismFiltered;
  }
  function onError(error) {
    console.log(`Error: ${error}`);
  }
  var sexismCheckbox = browser.storage.sync.get("SexismFiltered");
  sexismCheckbox.then(setCurrentChoice, onError);
}

function restoreFirstCustomCategory() {
  function setCurrentCategory(item) {
    firstCategory = document.getElementById("firstCategory");
    firstCategory.value = item.firstCustomSetting;
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
    secondCategory.value = item.secondCustomSetting;
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

var racism = document.getElementById("racism");
racism.addEventListener("change", function() {
  browser.storage.sync.set({
    RacismFiltered: racism.checked
  });
});

var sexism = document.getElementById("sexism");
sexism.addEventListener("change", function() {
  browser.storage.sync.set({
    SexismFiltered: sexism.checked
  });
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
document.addEventListener("DOMContentLoaded", restoreRacismCategory);
document.addEventListener("DOMContentLoaded", restoreSexismCategory);
document.addEventListener("DOMContentLoaded", restoreFirstCustomCategory);
document.addEventListener("DOMContentLoaded", restoreSecondCustomCategory);