require("jquery");
require('bootstrap'); //bootbox not self contained!!
//please read the bootbox documentation !!
var bootbox = require('bootbox');
text = window.getSelection().toString();
bootbox.dialog({
    title: 'Report Incorrect Classification',
    message: "<p>Please select the category of hate speech <q>" + text + "</q> belongs to:</p>",
    closeButton: false,
    size: 'large',
    buttons: {
        racist: {
            label: "Racist",
            callback: function(){
               const apiUrl = "https://mpymvmyfh0.execute-api.us-east-1.amazonaws.com/default/saveIncorrectHatespeech";
                let fetchData = {
                  method: "POST",
                  body: JSON.stringify(
                    {
                      "sentence": text,
                      "label": "Racist"
                    }
                  ),
                  headers: {
                    "Content-Type": "application/json"
                  }
                };
                return fetch(apiUrl, fetchData);
            }
        },
        sexist: {
            label: "Sexist",
            callback: function(){
              const apiUrl = "https://mpymvmyfh0.execute-api.us-east-1.amazonaws.com/default/saveIncorrectHatespeech";
               let fetchData = {
                 method: "POST",
                 body: JSON.stringify(
                   {
                     "sentence": text,
                     "label": "Sexist"
                   }
                 ),
                 headers: {
                   "Content-Type": "application/json"
                 }
               };
               return fetch(apiUrl, fetchData);
            }
        },
        offensive: {
            label: "Offensive",
            callback: function(){
              const apiUrl = "https://mpymvmyfh0.execute-api.us-east-1.amazonaws.com/default/saveIncorrectHatespeech";
               let fetchData = {
                 method: "POST",
                 body: JSON.stringify(
                   {
                     "sentence": text,
                     "label": "Offensive"
                   }
                 ),
                 headers: {
                   "Content-Type": "application/json"
                 }
               };
               return fetch(apiUrl, fetchData);
            }
        },
        nonoffensive: {
            label: "Non-offensive",
            callback: function(){
              const apiUrl = "https://mpymvmyfh0.execute-api.us-east-1.amazonaws.com/default/saveIncorrectHatespeech";
               let fetchData = {
                 method: "POST",
                 body: JSON.stringify(
                   {
                     "sentence": text,
                     "label": "Non-offensive"
                   }
                 ),
                 headers: {
                   "Content-Type": "application/json"
                 }
               };
               return fetch(apiUrl, fetchData);
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
