const detect_new_content = function(mutations) {
  mutations.forEach(function(mutation) {
    for (var i = 0; i < mutation.addedNodes.length; i++) {
        hatespeech_detection(mutation.addedNodes[i]);
    }
  });
};
//visited once per page
function walkNodeTree(root) {
  const nodes = [];
  node = root;
  start: while (node) {
      if(node.nodeType === Node.TEXT_NODE && !['STYLE', 'SCRIPT'].includes(node.nodeName)){
          nodes.push(node);
      } else{
          const observer = new MutationObserver(detect_new_content);
          // Start observing the target node for configured mutations
          observer.observe(node, {childList: true});
          // Later, you can stop observing
          // observer.disconnect();
          if (node.firstChild) {
            node = node.firstChild;
            continue start;
          }
      }
      while (node) {
          if (node === root) {
              break start;
          }

          if (node.nextSibling) {
              node = node.nextSibling;
              continue start;
          }

          node = node.parentNode;
      }
  }
  return nodes;
}

//TODO: 1. API for back end -- failed to remove parent nodes, use stream of text
//2. deal with new contents on the page -- example : stack overflow expand comments, reddit

function hatespeech_detection(root){
  function onError(error) {
    alert(`Error: ${error}`);
  }
  function onGot(item) {
    if(item.HateSpeechOn){
      var allText = walkNodeTree(root); //visit the dom
      str = ""
      for (i = 0; i < allText.length; i++) {
          allText[i].parentNode.style.color = getRandomColor();
          str = str + allText[i].nodeValue;
      }
      console.log(str); //all the string on the webpage

      var request = new XMLHttpRequest();
      request.open('GET', '/getmethod', true);
      request.setRequestHeader('Content-Type', 'application/json');
      request.send(JSON.stringify({"htmltext": str}));

      result = [234, 435];//call backend, get an array of intgers (the position of hate speech)
      pos = 0;
      hateSpeechIndex = 0;
      for(i = 0; i < allText.length; i++){
          pos += allText[i].length;
          if(pos >= result[hateSpeechIndex]){
            allText[i].parentNode.classList.add('blurry-text');
            hateSpeechIndex++;
          }
          if(hateSpeechIndex >= result.length){
            break;
          }
      }
    }
  }
  var getting = browser.storage.sync.get("HateSpeechOn");
  getting.then(onGot, onError);
}

document.addEventListener('DOMContentLoaded', (event) => {
  var style = document.createElement('style');
  style.type = 'text/css';
  style.innerHTML = '.blurry-text {\nfilter:blur(5px);\n}\n' +
                    '.blurry-text:hover {\nfilter:none;\n}';
  document.getElementsByTagName('head')[0].appendChild(style);
  hatespeech_detection(document.body);
});

function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}
