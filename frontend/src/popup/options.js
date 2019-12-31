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
    firstCategory.innerHTML = "";
    for(var i = 0; i < item.firstCustomSetting.length; i++) {
      let li = document.createElement("li");
      li.innerHTML = item.firstCustomSetting[i]  + " - ";

      let deleteLink = document.createElement("a");
      deleteLink.href = "#";
      deleteLink.innerHTML = "X";
      deleteLink.id = item.firstCustomSetting[i];

      deleteLink.addEventListener("click", function() {
        let elementToDelete = deleteLink.id;
        deleteItem(elementToDelete);
      });

      li.appendChild(deleteLink);

      firstCategory.appendChild(li);

      //firstCategory.innerHTML =  firstCategory.innerHTML + "<li>" + item.firstCustomSetting[i] + "</li>";
    }
  }

  function onError(error) {
    console.log(`Error: ${error}`);
  }

  var firstCustomSetting = browser.storage.sync.get("firstCustomSetting");
  firstCustomSetting.then(setCurrentCategory, onError);
}

function deleteItem(item) {
  let existingCats = browser.storage.sync.get("firstCustomSetting", function(setting) {
    let settings = setting.firstCustomSetting;
    let newSettings = settings.filter(set => item != set);
    browser.storage.sync.set({
      firstCustomSetting: newSettings
    });

    restoreFirstCustomCategory();
  });
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
  //browser.storage.sync.set({firstCustomSetting: []});
  console.log("ewewewew");
  let existingCats = browser.storage.sync.get("firstCustomSetting", function(setting) {
    console.log("lmao");
    if(setting.firstCustomSetting == null) {
      console.log("dude pls");
      setting = [];
    } else {
      let midValue = setting.firstCustomSetting;
      setting = midValue;
    }

    console.log(setting);

    let newCat = document.getElementById("firstCategory").value;

    console.log("puiuuu " + newCat);
    if(setting.includes(newCat)) {
      return
    }
    setting.push(newCat);

    browser.storage.sync.set({
      firstCustomSetting: setting
    });
    document.getElementById("firstCategory").value = "";
    restoreFirstCustomCategory();
  });
}

document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('addBtn');
    // onClick's logic below:
    btn.addEventListener('click', function() {
        addCategory();
        browser.tabs.reload();
    });
});

document.addEventListener("DOMContentLoaded", restoreOptions);
document.addEventListener("DOMContentLoaded", restoreFirstCustomCategory);
