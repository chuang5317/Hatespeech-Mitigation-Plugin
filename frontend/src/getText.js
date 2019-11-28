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
    !["STYLE", "SCRIPT"].includes(node.parentNode.nodeName);
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
      populateNodeManager(node);
    }

    // Then run hate speech detection.
    for (let node of mutation.addedNodes) {
      detectHatespeech(node);
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
      observer.observe(node, { childList: true });
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
function fetchHatespeechInfo(data) {
  const apiUrl = 'http://127.0.0.1:5000';
  // const apiUrl =
  //   "https://jmxk0e6pqd.execute-api.eu-west-2.amazonaws.com/Production/sentiment";

  let fetchData = {
    method: "POST",
    body: JSON.stringify(data),
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

function getChildNodeIndex(child){
  var i = 0;
  while( (child = child.previousSibling) != null ) 
    i++;
  return i;
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
          str = str + allText[i].nodeValue;
      }
      // console.log(nodesToJson)
      // Fetch the ranges to blur from the locally running service
      const response = fetchHatespeechInfo(str);
      // console.log("here");
      response
        .then(response => {
          if (!response.ok) {
            throw Error(response.statusText);
          }
          return response;
        })
        .then(response => {
          response.json().then(result => {
            pos = 0;
            hateSpeechIndex = 0;
            i = 0;
            for(i = 0; i < allText.length; i++){
              oldPos = pos;
              pos += allText[i].length;
              tempPos = pos;
              start = result[hateSpeechIndex][0];
              end = result[hateSpeechIndex][1];
              if(pos >= start && pos <= end){
                textNodePosInParent = getChildNodeIndex(allText[i]);
                lower = Math.max(result[hateSpeechIndex][0] - oldPos, 0);
                upper = Math.max(result[hateSpeechIndex][1] - pos, 0);
                nodeValue = allText[i].nodeValue;
                prevText = nodeValue.substr(oldPos, lower);
                curText = nodeValue.substr(lower, upper);
                afterText = nodeValue.substr(upper, pos);
                // console.log("lower is " + lower + ", upper is" + upper);
                // console.log("text in node :" + allText[i].nodeValue);
                // console.log("prevText :" + prevText  + " size is " + prevText.length);
                // console.log("curText :" + curText + " size is " + curText.length);
                // console.log("afterText :" + afterText + " size is " + afterText.length);
                parentNode = allText[i].parentNode;
                nextNode = allText[i].nextSibling;
                allText[i].remove();
                if(prevText.length > 0){
                  prevNode = document.createTextNode(prevText);
                  parentNode.insertBefore(prevNode, nextNode);
                }
                blurNode = document.createElement("a");
                blurNode.appendChild(document.createTextNode(curText));
                blurNode.classList.add('blurry-text');
                parentNode.insertBefore(blurNode, nextNode);
                if(afterText.length > 0){
                  afterNode = document.createTextNode(afterText);
                  parentNode.insertBefore(afterNode, nextNode);
                  //in case of multiple sentences in one node: 
                  allText[i] = afterNode;
                  pos -= allText[i].length;
                  i--;
                }
              }
              if(tempPos > end){
                hateSpeechIndex++;
              }
              if(hateSpeechIndex >= result.length){
                break;
              }
            }
          });
        })
        .catch(error => {
          console.log(error);
        });
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

// Note to self: DOMContentLoaded is when the initial HTML document is completely loaded and parsed,
// WITHOUT waiting for stylesheets, images and subframes to finish loading, as opposed to the usual "load".
document.addEventListener("DOMContentLoaded", event => {
  var style = document.createElement("style");
  style.type = "text/css";
  style.innerHTML =
    ".blurry-text {\nfilter:blur(5px);\n}\n" +
    ".blurry-text:hover {\nfilter:none;\n}";
  document.getElementsByTagName("head")[0].appendChild(style);

  populateNodeManager(document.body);
  detectHatespeech(document.body);
});
