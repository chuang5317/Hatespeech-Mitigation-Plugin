/**
 * Callback for detecting hatespeech when the DOM tree is updated.
 * @param mutations - an array of MutationRecord objects describing each change.
 */
function detect_new_content(mutations) {
  mutations.forEach(mutation => {
    for (let i = 0; i < mutation.addedNodes.length; i++) {
      hatespeech_detection(mutation.addedNodes[i]);
    }
  });
}

/**
 * Traverse the DOM tree and collect text nodes.
 * @param {*} root
 */
function walkNodeTree(root) {
  const nodes = [];
  node = root;
  start: while (node) {
    if (
      node.nodeType === Node.TEXT_NODE &&
      !["STYLE", "SCRIPT"].includes(node.nodeName)
    ) {
      console.log(`${node.nodeName}, ${node.nodeType}`);
      nodes.push(node);
    } else {
      const observer = new MutationObserver(detect_new_content);
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
 * Should have a parameter later for passing in the text nodes.
 * May require a callback parameter in the future (e.g. blur)
 */
function fetchHatespeechInfo() {
  const apiUrl = "http://127.0.0.1:5000/getmethod";
  let xhr = new XMLHttpRequest();

  xhr.open("GET", apiUrl, true);
  // xhr.send(JSON.stringify({ htmltext: str }));
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
  blurRange = [234, 435];
  pos = 0;
  hateSpeechIndex = 0;
  for (const textNode of textNodes) {
    pos += textNode.length;
    if (pos >= result[hateSpeechIndex]) {
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
function hatespeech_detection(root) {
  function onError(error) {
    alert(`Error: ${error}`);
  }
  function onGot(item) {
    if (item.HateSpeechOn) {
      const allText = walkNodeTree(root); //visit the dom
      console.log(`Got ${allText.length} text nodes`);
      let str = "";
      for (const textNode of allText) {
        textNode.parentNode.style.color = getRandomColor();
        str = str + textNode.nodeValue;
      }
      console.log(str); //all the string on the webpage

      // Fetch the ranges to blur from the locally running service
      fetchHatespeechInfo();

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

// Dynamically add a blur style to the document's CSS
// Then run hatespeech.
document.addEventListener("DOMContentLoaded", event => {
  var style = document.createElement("style");
  style.type = "text/css";
  style.innerHTML =
    ".blurry-text {\nfilter:blur(5px);\n}\n" +
    ".blurry-text:hover {\nfilter:none;\n}";
  document.getElementsByTagName("head")[0].appendChild(style);
  hatespeech_detection(document.body);
});
