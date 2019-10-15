//visited once per page
function walkNodeTree(root) {
    const nodes = []; 
    node = root;
    start: while (node) {
        if(node.nodeType === Node.TEXT_NODE && !['STYLE', 'SCRIPT'].includes(node.nodeName)){
            nodes.push(node.parentNode);
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


document.addEventListener('DOMContentLoaded', (event) => {
  function onError(error) {
    alert(`Error: ${error}`);
  }

  function onGot(item) {
    // if(item.HateSpeechOn){
      var allText = walkNodeTree(document.body); //visit the dom
      for (i = 0; i < allText.length; i++) {
          allText[i].style.color = getRandomColor();
      }
    // }
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