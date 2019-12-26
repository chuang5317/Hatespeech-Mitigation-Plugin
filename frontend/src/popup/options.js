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
    let firstCategory = document.getElementById("cats_list");
    firstCategory.innerHTML = ""
    for(var i = 0; i < item.firstCustomSetting.length; i++) {
      firstCategory.innerHTML =  firstCategory.innerHTML + "<li>" + item.firstCustomSetting[i] + "</li>";
    }
  }

  function onError(error) {
    console.log(`Error: ${error}`);
  }

  var firstCustomSetting = browser.storage.sync.get("firstCustomSetting");
  firstCustomSetting.then(setCurrentCategory, onError);
}

function updateCategoryList(item) {

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
    if(setting.firstCustomSetting == null) {
      console.log("se hizo mierda");
      setting = [];
    } else {
      let midValue = setting.firstCustomSetting;
      setting = midValue;
    }

    console.log("dewd");

    let newCat = document.getElementById("firstCategory").value;

    console.log("puiuuu" + newCat);

    setting.push(newCat);
    console.log("pinche mamut");
    console.log(setting);

    browser.storage.sync.set({
      firstCustomSetting: setting
    });

    console.log("reeeee");
    restoreFirstCustomCategory();
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
