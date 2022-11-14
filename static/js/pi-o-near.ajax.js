"use strict";

function AjaxHandler(path, method){
  this.path   = path;
  this.method = method;
};

AjaxHandler.prototype = {
  doneHandler: function(msg){
    console.log("Command done: " + msg);
  },
  failHandler: function(){
    console.warn("Request fail");
  },
  sendRequest: function(command){
    if (typeof command !== 'string'){
      throw "Only string commands can be sent.";
      return false;
    };
    if (command === 'none'){
      return false;
    }
    $.ajax({
      method: this.method,
      url:    this.path,
      data:   {command: command}
    })
    .done(this.doneHandler)
    .fail(this.failHandler);
  }
};