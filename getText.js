function textNodesUnder(el) {
    return walkNodeTree(el, {
        inspect: n => !['STYLE', 'SCRIPT'].includes(n.nodeName),
        collect: n => (n.nodeType === 3)
    });
}

function walkNodeTree(root, options) {
    options = options || {};

    const inspect = options.inspect || (n => true),
          collect = options.collect || (n => true);
    const walker = document.createTreeWalker(
        root,
        NodeFilter.SHOW_ALL,
        {
            acceptNode: function(node) {
                if(!inspect(node)) { return NodeFilter.FILTER_REJECT; }
                if(!collect(node)) { return NodeFilter.FILTER_SKIP; }
                return NodeFilter.FILTER_ACCEPT;
            }
        }
    );

    const nodes = []; let n;
    while(n = walker.nextNode()) {
        options.callback && options.callback(n);
        nodes.push(n);
    }

    return nodes;
}


document.addEventListener('DOMContentLoaded', (event) => {
  function onError(error) {
    alert(`Error: ${error}`);
  }

  function onGot(item) {
    if(item.HateSpeechOn){
      var allText = textNodesUnder(document.body); //visit the dom
      for (i = 0; i < allText.length; i++) {
          allText[i].parentNode.style.color = "#000080";
      }
    }
  }
  var getting = browser.storage.sync.get("HateSpeechOn");
  getting.then(onGot, onError);
});
