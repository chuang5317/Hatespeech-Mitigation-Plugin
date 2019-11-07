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
 */
function initNodeManager() {
  // Apparently tree walker is the fastest way to get text nodes
  // https://stackoverflow.com/questions/2579666
  const walker = document.createTreeWalker(
    document.body,
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
    for (let node of mutation.addedNodes) {
      nodeManager.addNode(node);
    }

    for (let node of mutation.addedNodes) {
      detectHatespeech(node);
    }
  });
}

/**
 * Determine whether a node's text content is entirely whitespace.
 * Source: https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Whitespace_in_the_DOM
 *
 * @param node - the node to test
 * @return - True if all of the text content of `node` is whitespace, otherwise false.
 */
function isAllWhiteSpace(nod) {
  // Use ECMA-262 Edition 3 String and RegExp features
  return !/[^\t\n\r ]/.test(nod.textContent);
}

/**
 * Traverse the DOM tree and collect text nodes.
 * @param root - DOM root node.
 */
function walkNodeTree(root) {
  const nodes = [];
  let node = root;
  start: while (node) {
    if (node.nodeType === Node.TEXT_NODE && !isAllWhiteSpace(node)) {
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
 */
function fetchHatespeechInfo(str) {
  const apiUrl = "http://127.0.0.1:5000/getmethod";
  // const apiUrl = "http://127.0.0.1:5000/frontend-expt";
  let xhr = new XMLHttpRequest();

  xhr.open("GET", apiUrl, true);
  xhr.send(JSON.stringify({ htmltext: str }));
  xhr.onprogress = () => {};
  xhr.onload = () => {
    if (xhr.status !== 200) {
      console.log(`Error ${xhr.status}: ${xhr.statusText}`);
    } else {
      console.log(`Done, got ${xhr.response.length} bytes ${xhr.responseText}`);
    }
  };
  xhr.onerror = () => {
    console.log("Request failed");
  };
}

/**
 * Blur hatespeech.
 * @param textNodes - array of text nodes *
 * Should have a range parameter in the future, indicating which nodes to blur.
 */
function blurHatespeechNodes(textNodes) {
  // Range of hatespeech nodes to flag. Hard-coded, but it should be a real result from the backend
  let blurRange = [234, 435];
  let pos = 0;
  let hateSpeechIndex = 0;
  for (const textNode of textNodes) {
    pos += textNode.length;
    if (pos >= blurRange[hateSpeechIndex]) {
      textNode.parentNode.classList.add("blurry-text");
      hateSpeechIndex++;
    }
    if (hateSpeechIndex >= blurRange.length) {
      break;
    }
  }
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
      console.log(allText);
      let str = "";

      for (const textNode of allText) {
        textNode.parentNode.style.color = getRandomColor();
        str = str + textNode.nodeValue;
      }

      // Fetch the ranges to blur from the locally running service
      fetchHatespeechInfo(str);

      // May have to put this in the XMLHttpRequest callback: only blur onProgress.
      blurHatespeechNodes(allText);
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

  initNodeManager();
  detectHatespeech(document.body);
});
