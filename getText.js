//visited once per page
function walkNodeTree(root) {
    const nodes = []; 
    node = root;
    start: while (node) {
        if(node.nodeType === Node.TEXT_NODE && !['STYLE', 'SCRIPT'].includes(node.nodeName)){
            nodes.push(node);
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
    remove = [];
    nodes.forEach((n) => {
      p = n.parentNode.parentNode.parentNode;
      if(nodes.includes(p)){
        remove.push(p);
      }
    });
    return nodes.filter(function(n){
      return !remove.includes(n);
    });
    // return nodes;
}

//TODO: 1. API for back end -- failed to remove parent nodes, use stream of text
//2. deal with new contents on the page -- example : stack overflow expand comments, reddit 
//we may want to consider doing this plugin just for a specific website?

document.addEventListener('DOMContentLoaded', (event) => {
  function onError(error) {
    alert(`Error: ${error}`);
  }

  function onGot(item) {
    if(item.HateSpeechOn){
      var style = document.createElement('style');
      style.type = 'text/css';
      style.innerHTML = '.blurry-text {\nfilter:blur(2px);\n}';
      document.getElementsByTagName('head')[0].appendChild(style);
      var allText = walkNodeTree(document.body); //visit the dom
      for (i = 0; i < allText.length; i++) {
          allText[i].parentNode.classList.add('blurry-text');
          allText[i].parentNode.style.color = getRandomColor();
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