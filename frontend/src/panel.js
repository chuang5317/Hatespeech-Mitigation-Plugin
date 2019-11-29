require("jquery");
require('bootstrap'); //bootbox not self contained!!
//please read the bootbox documentation !!
var bootbox = require('bootbox');
text = window.getSelection().toString();
bootbox.dialog({
    title: 'Report incorrect classification',
    message: text,
    size: 'medium',
    buttons: {
        racist: {
            label: "Racist",
            callback: function(){
                //
            }
        },
        sexist: {
            label: "Sexist",
            callback: function(){
                //
            }
        },
        offensive: {
            label: "Offensive",
            callback: function(){
                //
            }
        },
        nonoffensive: {
            label: "Non-offensive",
            callback: function(){
                //
            }
        }, 
        close: {
            label: "Close",
            callback: function(){
                //
            }
        }
    }
});