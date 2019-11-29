//adding dependencies :
//bootstrap css

function readTextFile(file)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                return allText;
            }
        }
    }
    rawFile.send(null);
}

var link = document.createElement("link");
link.rel = "stylesheet";
link.type = "text/css";
link.href = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css";
link.integrity = "sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh";
link.crossOrigin="anonymous";
document.head.appendChild(link);

//JQuery
var scriptJquery = document.createElement("script");
scriptJquery.src = "https://code.jquery.com/jquery-3.4.1.slim.min.js";
scriptJquery.integrity = "sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n";
scriptJquery.crossOrigin = "anonymous";
document.body.appendChild(scriptJquery);

var scriptPopper = document.createElement("script");
scriptPopper.src = "https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js";
scriptPopper.integrity = "sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo";
scriptPopper.crossOrigin = "anonymous";
document.body.appendChild(scriptPopper);

var scriptBootStrap = document.createElement("script");
scriptBootStrap.src = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js";
scriptBootStrap.integrity = "sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6";
scriptBootStrap.crossOrigin = "anonymous";
document.body.appendChild(scriptBootStrap);

//bootbox
var scriptBootBox = document.createElement("script");
scriptBootBox.src = "https://cdnjs.cloudflare.com/ajax/libs/bootbox.js/5.3.2/bootbox.min.js";
document.body.appendChild(scriptBootBox);

var scriptDialog = document.createElement("script");
scriptDialog.type = "text/javascript";
file = readTextFile('file:///home/tianyi/newbranch/frontend/src/panel.js');
try {
    scriptDialog.appendChild(document.createTextNode(code));
} catch (e) {
    scriptDialog.text = code;
    document.body.appendChild(scriptDialog);
}

var button = document.createElement('button');
button.textContent = "CLICK ME PLEASE!";
button.id = "hatespeechhack";
document.body.appendChild(button);


// {
//     "matches": ["<all_urls>"],
//     "js": ["src/rightclick.js"]
//   },
