$(document).on("click", "#hatespeechhack", function(e) {
  alert("aloha");
  selectedText = window.getSelection().toString();
  bootbox.dialog({
    title: 'A custom dialog with buttons and callbacks',
    message: selectedText,
    size: 'large',
    buttons: {
        cancel: {
            label: "I'm a cancel button!",
            className: 'btn-danger',
            callback: function(){
                console.log('Custom cancel clicked');
            }
        },
        noclose: {
            label: "I don't close the modal!",
            className: 'btn-warning',
            callback: function(){
                console.log('Custom button clicked');
                return false;
            }
        },
        ok: {
            label: "I'm an OK button!",
            className: 'btn-info',
            callback: function(){
                console.log('Custom OK clicked');
            }
        }
    }
  });
})