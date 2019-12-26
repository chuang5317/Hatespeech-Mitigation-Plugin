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
    firstCategory = document.getElementById("cats_list");
    console.log(item);
    for(var i = 0; i < item.length; i++) {
      firstCategory.innerHTML =  "hola";
    }
  }

  function onError(error) {
    console.log(`Error: ${error}`);
  }

  var firstCustomSetting = browser.storage.sync.get("firstCustomSetting");
  firstCustomSetting.then(setCurrentCategory, onError);
}

var checkbox = document.getElementById("toggle-slider-input");
checkbox.addEventListener("change", function() {
  console.log(`Hatespeech detection set to ${checkbox.checked}.`);
  browser.storage.sync.set({
    HateSpeechOn: checkbox.checked
  });
  browser.tabs.reload();
});

function addCategory() {
  console.log("ewewewew");
  let existingCats = browser.storage.sync.get("firstCustomSetting", function(setting) {
    if(setting == null) {
      console.log("d00d pls");
      existingCats = array();
    }

    //console.log(existingCats);

    let newCat = document.getElementById("firstCategory").value;

    console.log(newCat);

    console.log("deed");
    setting.append(newCat);
    console.log("existingCats");
    console.log(setting);

    browser.storage.sync.set({
      firstCustomSetting: existingCats
    });
  });
}

document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('addBtn');
    // onClick's logic below:
    btn.addEventListener('click', function() {
        addCategory();
    });
});

document.addEventListener("DOMContentLoaded", restoreOptions);
document.addEventListener("DOMContentLoaded", restoreFirstCustomCategory);
