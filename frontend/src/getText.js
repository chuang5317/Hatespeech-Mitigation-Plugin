/**
 * Determine whether a node's text content is entirely whitespace.
 * Source: https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Whitespace_in_the_DOM
 *
 * @param node - the node to test
 * @return - True if all of the text content of `node` is whitespace, otherwise false.
 */
function isAllWhiteSpace(node) {
  // Use ECMA-262 Edition 3 String and RegExp features
  return !/[^\t\n\r ]/.test(node.textContent);
}

/**
 * Determine if a node is a meaningful text node.
 * @param node - a DOM node
 * @returns boolean
 */
function isUsefulNode(node) {
  // the text node within a SCRIPT Element node is javascript code
  // the text node within a STYLE Element node is CSS
  // We don't want these.
  let isParentOk =
    node.parentNode === null ||
    !["STYLE", "SCRIPT", "NOSCRIPT"].includes(node.parentNode.nodeName);
  return (
    node.nodeType === Node.TEXT_NODE && !isAllWhiteSpace(node) && isParentOk
  );
}

/**
 * Keeps track of DOM nodes and node ids.
 *
 * NOTE: this is ES6 syntax.
 */
class NodeManager {
  constructor() {
    this.nodeIDCount = 0;
    this.nodeIDMap = new Map();
  }

  addNode(node) {
    this.nodeIDMap.set(this.nodeIDCount, node);
    ++this.nodeIDCount;
  }

  getNode(nodeID) {
    return this.nodeIDMap.get(nodeID);
  }

  getID(node) {
    // TODO: not efficient, will experiment
    for (const nodeID of this.nodeIDMap.keys()) {
      if (this.nodeIDMap.get(nodeID) === node) {
        return nodeID;
      }
    }
    return undefined;
  }
}

/**
 * Initialise the node ID manager. To be called in a DOMContentLoaded listener.
 * @param root - root node to start recursively adding from
 */
function populateNodeManager(root) {
  // Apparently tree walker is the fastest way to get text nodes
  // https://stackoverflow.com/questions/2579666
  const walker = document.createTreeWalker(
    root,
    NodeFilter.SHOW_TEXT,
    // NodeFilter.SHOW_ALL,
    null,
    false
  );
  let node;
  while ((node = walker.nextNode())) {
    nodeManager.addNode(node);
  }
}

const nodeManager = new NodeManager();

/**
 * Callback for detecting hatespeech when the DOM tree is updated.
 * @param mutations - an array of MutationRecord objects describing each change.
 */
function onNewContentAdded(mutations) {
  mutations.forEach(mutation => {
    // Need to recursively assign new text node IDs.
    for (let node of mutation.addedNodes) {
      if(node.updated != true){
        populateNodeManager(node);
      }
    }

    // Then run hate speech detection.
    for (let node of mutation.addedNodes) {
      if(node.updated != true){
        detectHatespeech(node);
      }
    }
  });
}

/**
 * Traverse the DOM tree and collect text nodes.
 * @param root - DOM root node.
 */
function walkNodeTree(root) {
  const nodes = [];
  let node = root;
  start: while (node) {
    if (isUsefulNode(node)) {
      nodes.push(node);
    } else {
      const observer = new MutationObserver(onNewContentAdded);
      // Start observing the target node for configured mutations
      observer.observe(node, {
        childList: true
      });
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

/**
 * Retrieve results from the hate speech NLP service.
 *
 * @param str - string of text to send to service.
 *
 * @returns - a Promise object that will contain a response object if successfull.
 */
function fetchHatespeechInfo(data, callback) {
  const apiUrl = 'http://main.fm6pxzwu77.eu-west-2.elasticbeanstalk.com/';
  let fetchData = {
    method: "POST",
    body: data,
    headers: {
        "Content-Type": "text/plain"
    }
  };
  return fetch(apiUrl, fetchData);
}

/**
 * Blur the entirety of one text node.
 * @param textNode - a Text Node
 */
function blurNode(textNode) {
  textNode.parentNode.classList.add("blurry-text");
}

function getChildNodeIndex(child) {
  var i = 0;
  while ((child = child.previousSibling) != null)
    i++;
  return i;
}

function hasKeyword(keyword, sentence) {
    return sentence.indexOf(keyword.toLowerCase()) > -1;
}

/**
 * Run hate speech checking over the DOM Tree.
 * @param root - DOM root node
 */
function detectHatespeech(root) {
  function onError(error) {
    alert(`Error: ${error}`);
  }

  function onGot(item) {
    if (item.HateSpeechOn) {
      const allText = walkNodeTree(root); //visit the dom
      let str = "";
      for (let i = 0; i < allText.length; i++) {
        let new_str = allText[i].nodeValue;
        for (let j = 0; j < keywords.length; j++){
          if (hasKeyword(keywords[j], new_str)) {
          nodeValue = allText[i].nodeValue;
          nextNode = allText[i].nextSibling;
          allText[i].remove();

          blurNode = document.createElement("span");
          blurNode.appendChild(document.createTextNode(curText));
          blurNode.updated = true;
          blurNode.classList.add('blurry-text');
          parentNode.insertBefore(blurNode, nextNode);
          }
        }
        str = str + new_str;
      }



      // Fetch the ranges to blur from the running service
      if(str.length > 0){
        const response = fetchHatespeechInfo(str);
        response
        .then(response => {
          if (!response.ok) {
	    console.log(response);
            throw Error(response.statusText);
          }
          return response;
        })
        .then(response => {
          //Travel through the nodes and find the positions that hatespeech appears
          response.json().then(result => {
            pos = 0;
            hateSpeechIndex = 0;
            i = 0;
            for (i = 0; i < allText.length && hateSpeechIndex < result.length; i++) {
              oldPos = pos; //the starting position of the node
              pos += allText[i].nodeValue.length; //the end position of the node
              //skipping the previous hatespeech
              while (oldPos >= result[hateSpeechIndex][1]) {
                hateSpeechIndex++;
              }
              start = result[hateSpeechIndex][0]; //start of the current hatespeech
              //if this node conatins multiple hatespeech, treat them as one
              while (pos > result[hateSpeechIndex][1]){
                hateSpeechIndex++;
              }
              end = result[hateSpeechIndex][1]; //the end of the hatespeech
              lower = Math.max(start - oldPos, 0); //the lower index of the hatespeech in this node
              upper = Math.min(end - oldPos, allText[i].length);//upper
              nodeValue = allText[i].nodeValue; //text in the node
              curText = nodeValue.substr(lower, upper); //the part to blur
              if(curText.length > 0){ // if there are nothing to blur, don't change anything
                prevText = nodeValue.substr(0, lower); //text before blur
                afterText = nodeValue.substr(upper, allText[i].length); //text after blur
                parentNode = allText[i].parentNode; //the parent of the original text node
                nextNode = allText[i].nextSibling; // the node after the original node
                allText[i].remove(); //remove the original node in the DOM tree
                
                if (prevText.length > 0) {// if there is text before the blur text, insert it
                  prevNode = document.createTextNode(prevText);
                  prevNode.updated = true;
                  parentNode.insertBefore(prevNode, nextNode);
                }

                //insert the blur text
                blurNode = document.createElement("span");
                blurNode.appendChild(document.createTextNode(curText));
                blurNode.updated = true;
                blurNode.classList.add('blurry-text');
                parentNode.insertBefore(blurNode, nextNode);

                // if there is text after the blur text, insert it
                if (afterText.length > 0) {
                  afterNode = document.createTextNode(afterText);
                  afterNode.updated = true;
                  parentNode.insertBefore(afterNode, nextNode);
                }
              }
            }
          });
        })
        .catch(error => {
          console.log(error);
        });
      }
    }
  }
  var getting = browser.storage.sync.get("HateSpeechOn");
  getting.then(onGot, onError);
}

/**
 * Temporary debugging helper function.
 */
function getRandomColor() {
  var letters = "0123456789ABCDEF";
  var color = "#";
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

function injectBootstrapCSS() {
	var link = document.createElement("link");
	link.rel = "stylesheet";
	link.type = "text/css";
	link.href = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css";
	link.integrity = "sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh";
	link.crossOrigin = "anonymous";
	document.head.appendChild(link);
}

// Note to self: DOMContentLoaded is when the initial HTML document is completely loaded and parsed,
// WITHOUT waiting for stylesheets, images and subframes to finish loading, as opposed to the usual "load".
document.addEventListener("DOMContentLoaded", event => {

  function onError(error) {
    console.log(`Error: ${error}`);
  }

  function onGot(item) {
    var style = document.createElement("style");
    style.type = "text/css";
    if (item.RevealOnHover) {
      style.innerHTML = ".blurry-text {\nfilter:blur(5px);\n}\n";
    } else {
      style.innerHTML =
        ".blurry-text {\nfilter:blur(5px);\n}\n" +
        ".blurry-text:hover {\nfilter:none;\n}";
    }
    document.getElementsByTagName("head")[0].appendChild(style);
    injectBootstrapCSS();
  }

  var getting = browser.storage.sync.get("RevealOnHover");
  getting.then(onGot, onError);

  populateNodeManager(document.body);
  detectHatespeech(document.body);
});
