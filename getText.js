//visited once per page
function walkNodeTree(root) {
    const nodes = []; 
    node = root;
    start: while (node) {
        if(node.nodeType === Node.TEXT_NODE && !['STYLE', 'SCRIPT'].includes(node.nodeName)){
          parent = node.parentNode;
          if(parent.firstChild != parent.lastChild || !['P'].includes(parent.nodeName)){ //more than 1 child (the text) or is paragraph
            nodes.push(parent);
          }
        } else{
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

//TODO: 1. find a way to remove useless parent nodes -- otherwise we may read same content multiple times
//2. deal with new contents on the page -- example : stack overflow expand comments, reddit 
//we may want to consider doing this plugin just for a specific website?

document.addEventListener('DOMContentLoaded', (event) => {
  function onError(error) {
    alert(`Error: ${error}`);
  }

  function onGot(item) {
    if(item.HateSpeechOn){
      var allText = walkNodeTree(document.body); //visit the dom
      for (i = 0; i < allText.length; i++) {
          allText[i].style.color = getRandomColor();
      }
    }
  }
  var getting = browser.storage.sync.get("HateSpeechOn");
  getting.then(onGot, onError);
});

function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}