"use strict";

/*Radio buttons that alter driving controllers*/

function DrivingChoice(domObj, ajaxHandler){
  this.domObj      = domObj;
  this.ajaxHandler = ajaxHandler;
  this.bindEvents();
  this.init();
};

DrivingChoice.prototype = {
  bindEvents: function(){
    var self = this;
    $(this.domObj).find('input[type=radio]').bind('change', function(){
      if ($(this).prop('checked')){
        var thisValue = $(this).prop('value');
        $('.driveing-option-wrapper').hide();
        $("#driving_option_" + thisValue).show();
        $('.listen-for-change').trigger('change');  /* Specific elements are listening for this and will reinitiate */
        self.ajaxHandler.sendRequest('init');       /* Initiate the car with the default values */
      };
    });
  },
  init: function(){
    // .eq(0) for the first set of controls (change to initiate with different set)
    $(this.domObj).find('input[type=radio]').eq(0).prop('checked','checked').change();
  }
};


/*Buttons*/

function CarButton(domObj, ajaxHandler){
  this.domObj       = domObj;
  this.onCommand    = $(this.domObj).data('oncommand');    /*Command on buttondown*/
  this.offCommand   = $(this.domObj).data('offcommand');   /*Command on buttonup*/
  this.key          = $(this.domObj).data('key');          /*Keyboard keycode associated with that button*/
  this.ajaxHandler  = ajaxHandler;
  this.isMobile     = window.mobilecheck();
  this.triggered    = false;                               /*This is used as a flag so that we don't send multiple requests on keyhold*/
  this.bindEvents();
};

CarButton.prototype = {
  bindEvents: function(){
    this.bindOnCommand();
    this.bindOffCommand();
    this.bindVisualEvents();
  },
  bindOnCommand: function(){
    if (this.isMobile){
      this.bindOnCommandMobile();
    }
    else{
      this.bindOnCommandDesktop();
    }
  },
  bindOnCommandMobile: function(){
    var self = this;
    $(this.domObj).bind('touchstart', function(){
      self.ajaxHandler.sendRequest(self.onCommand);
    });
  },
  bindOnCommandDesktop: function(){
    var self = this;
    $(this.domObj).bind('mousedown', function(){
      self.ajaxHandler.sendRequest(self.onCommand);
    });
    $(document).bind('keydown', function(event){
      if (event.which === self.key){
        if (!self.triggered){
          self.ajaxHandler.sendRequest(self.onCommand);
        }
        self.triggered = true;
        event.preventDefault();
      };
    });
  },
  bindOffCommand: function(){
    if (this.isMobile){
      this.bindOffCommandMobile();
    }
    else{
      this.bindOffCommandDesktop();
    }
  },
  bindOffCommandMobile: function(){
    var self = this;
    $(this.domObj).bind('touchend', function(){
      self.ajaxHandler.sendRequest(self.offCommand);
    });
  },
  bindOffCommandDesktop: function(){
    var self = this;
    $(this.domObj).bind('mouseup', function(){
      self.ajaxHandler.sendRequest(self.offCommand);
    });
    $(document).bind('keyup', function(event){
      if (event.which === self.key){
        self.triggered = false;
        self.ajaxHandler.sendRequest(self.offCommand);
        event.preventDefault();
      };
    });
  },
  bindVisualEvents: function(){
    if (this.isMobile){
      this.bindVisualEventsMobile();
    }
    else{
      this.bindVisualEventsDesktop();
    }
  },
  bindVisualEventsMobile: function(){
    var self = this;
    $(self.domObj).bind('touchstart', function(){
      $(self.domObj).addClass('button-active');
    });
    $(self.domObj).bind('touchend', function(){
      $(self.domObj).removeClass('button-active');
    });
  },
  bindVisualEventsDesktop: function(){
    var self = this;
    $(self.domObj).bind('mouseover', function(){
      $(self.domObj).addClass('button-hover');
    });
    $(self.domObj).bind('mouseout', function(){
      $(self.domObj).removeClass('button-hover');
    });
    $(self.domObj).bind('mousedown', function(){
      $(self.domObj).addClass('button-active');
    });
    $(document).bind('mouseup', function(){
      $(self.domObj).removeClass('button-active');
    });
  }
};


/*Slider for adjusting the speed*/

function SpeedSlider(domObj, ajaxHandler){
  this.domObj       = domObj;
  this.slider       = $(this.domObj).find("#speed_slider");
  this.sliderValue  = $(this.domObj).find("#speed_value");
  this.ajaxHandler  = ajaxHandler;
  this.setSlider();
  this.bindEvents();
};

SpeedSlider.prototype = {
  setSlider: function(){
    var self = this;
    $(self.slider).slider({
      'orientation': 'horizontal',
      'min':         0,
      'max':         100,
      'step':        1,
      'value':       50,
      'change': function(){
        var value = $(this).slider('value');
        $(self.sliderValue).html(value);
        self.ajaxHandler.sendRequest("speed_" + value);
      },
      'slide': function(){
        var value = $(this).slider('value');
        $(self.sliderValue).html(value);
      }
    });
  },
  bindEvents: function(){
    var self = this;
    $(self.slider).bind('change', function(){
      self.init();
    });
  },
  init: function(){
    $(this.slider).slider('value','50');
  }
};



/*Joystick controller*/

function DrivingJoystick(domObj, ajaxHandler){
  this.domObj         = domObj;
  this.ajaxHandler    = ajaxHandler;
  this.bounds         = $(this.domObj).find('.joystick-boundaries');
  this.grip           = $(this.domObj).find('.joystick-grip');
  this.boundsWidth    = $(this.bounds).innerWidth();
  this.boundsHeight   = $(this.bounds).innerHeight();
  this.isMobile       = window.mobilecheck();
  this.dragging       = false;  /*Used as a flag to know whether the grip is active or not (should we move it or not)*/
  this.direction      = 'none'; /*Used to monitor the movement direction so that we request a direction change only when necessary*/
  this.lastSpeed      = 0;      /*Used to filter the speed commands so that we send fewer requests to the server*/
  this.lastTurn       = 0;      /*Used to filter the steer commands so that we send fewer requests to the server*/
  this.turnFilterGap  = 10;     /*Defines the gap for the valid requests for steering. A value of 10 means that only 100/10 commands can be generated*/
  this.speedFilterGap = 20;     /*Defines the gap for the valid requests for speed. A value of 20 means that only 100/20 commands can be generat*/
  this.bindEvents();
};

DrivingJoystick.prototype = {
  bindEvents: function(){
    if (this.isMobile){
      this.bindVisualsMobile();
      this.bindDragListenerMobile();
      this.bindMovementsMobile();
    }
    else{
      this.bindVisualsDesktop();
      this.bindDragListenerDesktop();
      this.bindMovementsDesktop();
    }
  },
  bindVisualsDesktop: function(){
    var self = this;
    $(self.grip).bind('mouseover', function(){
      $(self.grip).addClass('joystick-grip-hover');
    });
    $(self.grip).bind('mouseout', function(){
      $(self.grip).removeClass('joystick-grip-hover');
    });
    $(self.grip).bind('mousedown', function(){
      $(self.grip).addClass('joystick-grip-active');
    });
    $(document).bind('mouseup', function(){
      $(self.grip).removeClass('joystick-grip-active');
    });
  },
  bindDragListenerDesktop: function(){
    var self = this;
    $(self.grip).bind('mousedown', function(){
      self.init();
      self.dragging = true;
    });
    $(document).bind('mouseup', function(){
      if (self.dragging){
        self.dragging = false;
        self.releaseGrip();
      };
    });
  },
  bindVisualsMobile: function(){
    var self = this;
    $(this.grip).bind('touchstart', function(){
      $(this).addClass('joystick-grip-active');
    });
    $(this.grip).bind('touchend', function(){
      $(this).removeClass('joystick-grip-active');
    });
  },
  bindDragListenerMobile: function(){
    var self = this;
    $(this.grip).bind('touchstart', function(){
      self.init();
      self.dragging = true;
    });
    $(this.grip).bind('touchend', function(){
      self.dragging = false;
      self.releaseGrip();
    });
  },
  releaseGrip: function(){
    var coordinates = {
      x: 0,
      y: 0
    };
    this.moveGrip(coordinates);
    this.processCommand(coordinates);
  },
  bindMovementsDesktop: function(){
    var self = this;
    $(document).bind('mousemove', function(event){
      if (!self.dragging){
        return false;
      };
      var mouseX              = event.clientX;
      var mouseY              = event.clientY;
      var relativeCoordinates = self.getRelativeCoordinates(mouseX, mouseY);
      self.moveGrip(relativeCoordinates);
      self.processCommand(relativeCoordinates);
    });
  },
  bindMovementsMobile: function(){
    var self = this;
    $(document).bind('touchmove', function(event){
      if (self.dragging){
        var mouseX              = event.targetTouches[0].clientX;
        var mouseY              = event.targetTouches[0].clientY;
        var relativeCoordinates = self.getRelativeCoordinates(mouseX, mouseY);
        self.moveGrip(relativeCoordinates);
        self.processCommand(relativeCoordinates); 
        return false;
      };
    });
  },
  getRelativeCoordinates: function(mouseX, mouseY){
    var boundsOffsetX = parseInt($(this.bounds).offset().left);
    var boundsOffsetY = parseInt($(this.bounds).offset().top);
    var boundsX       = boundsOffsetX - $(window).scrollLeft();
    var boundsY       = boundsOffsetY - $(window).scrollTop();
    var boundsCenterX = boundsX + this.boundsWidth/2;
    var boundsCenterY = boundsY + this.boundsHeight/2;
    var coordinatesX  = mouseX - boundsCenterX;
    var coordinatesY  = boundsCenterY - mouseY;
    if (coordinatesX > this.boundsWidth/2){
      coordinatesX = this.boundsWidth/2;
    }
    if (coordinatesX < -this.boundsWidth/2){
      coordinatesX = -this.boundsWidth/2;
    }
    if (coordinatesY > this.boundsHeight/2){
      coordinatesY = this.boundsHeight/2;
    }
    if (coordinatesY < -this.boundsHeight/2){
      coordinatesY = -this.boundsHeight/2;
    }
    return {
      x: coordinatesX,
      y: coordinatesY
    };
  },
  moveGrip: function(coordinates){
    var cssLeft       = coordinates.x + this.boundsWidth/2;
    var cssTop        = this.boundsHeight/2 - coordinates.y;
    $(this.grip).css({
      'left': cssLeft,
      'top':  cssTop
    });
  },
  processCommand: function(coordinates){
    var gripX         = coordinates.x;
    var gripY         = coordinates.y;
    /*The following two lines map the coordinates to a 0-100 range*/
    var percentX      = parseInt((gripX + this.boundsWidth/2)*100/this.boundsWidth);
    var percentY      = parseInt(Math.abs(gripY)*100/(this.boundsHeight/2));
    this.executeCommand('speed_' + percentY);
    this.executeCommand('turn_' + percentX);
    if (gripY > 0){
      if (this.direction !== 'fwd'){
        this.direction = 'fwd';
        this.executeCommand('move_fwd');
      }
    }
    else if (gripY < 0){
      if (this.direction !== 'bwd'){
        this.direction = 'bwd';
        this.executeCommand('move_bwd');
      }
    }
    else{
      if (this.direction !== 'none'){
        this.direction = 'none';
        this.executeCommand('move_stop');
      }
    }
  },
  executeCommand: function(command){
    command = this.filterCommands(command);
    this.ajaxHandler.sendRequest(command);
  },
  filterCommands: function(command){
    /* Since sending all gripmoves will flood the server, we filter and send only the important ones */
    /* We filter only speed and steer which are constantly changing and send only when the new value */
    /* is not in the same gap as the previous one. The gap is defined by speedFilterGap and turnFilterGap */
    if (command.startsWith("speed_")){
      var newSpeed = parseInt(command.replace('speed_',''))
      newSpeed = Math.round(newSpeed/this.speedFilterGap)*this.speedFilterGap /* Converts in one of the gap boundaries*/
      if (newSpeed != this.lastSpeed){
        this.lastSpeed = newSpeed
        return "speed_" + newSpeed
      }
      else{
        return "none"
      }
    }
    else if (command.startsWith("turn_")){
      var newTurn = parseInt(command.replace('turn_',''))
      newTurn = Math.round(newTurn/this.turnFilterGap)*this.turnFilterGap /* Converts in one of the gap boundaries*/
      if (newTurn != this.lastTurn){
        this.lastTurn = newTurn
        return "turn_" + newTurn
      }
      else{
        return "none"
      }
    }
    else{
      return command;
    }
  },
  init: function(){
    this.ajaxHandler.sendRequest('move_stop');
    this.ajaxHandler.sendRequest('turn_50');
    this.ajaxHandler.sendRequest('speed_0');
  }
};


/*Accelerometer*/

function Accelerometer(domObj, ajaxHandler){
  this.domObj         = domObj;
  this.ajaxHandler    = ajaxHandler;
  this.enabled        = false;  /*Used to flag whether the accelerometer is active or not*/
  this.direction      = 'none'; /*Used to monitor the movement direction so that we request a direction change only when necessary*/
  this.lastSpeed      = 0;      /*Used to filter the speed commands so that we send fewer requests to the server*/
  this.lastTurn       = 0;      /*Used to filter the steer commands so that we send fewer requests to the server*/
  this.turnFilterGap  = 10;     /*Defines the gap for the valid requests for steering. A value of 25 means that only 100/25 commands can be generated*/
  this.speedFilterGap = 20;     /*Defines the gap for the valid requests for speed. A value of 20 means that only 100/20 commands can be generat*/
  this.bindEvents();
};

Accelerometer.prototype = {
  bindEvents: function(){
    this.bindTouch()
    this.bindMovements();
  },
  bindTouch: function(){
    var self = this;
    $(this.domObj).bind('touchend', function(){
      self.vibrate();
      if (self.enabled){
        $(this).removeClass('phone-accelerometer-active');
        self.enabled = false;
      }
      else{
        $(this).addClass('phone-accelerometer-active');
        self.init();
        self.enabled = true;
      };
    });
  },
  bindMovements: function(){
    var self = this;
    window.addEventListener("devicemotion",
                            function(event){
                              self.processMovement(event);
                            },
                            false);
  },
  processMovement: function(event){
    if (!this.enabled){
      this.processStop();
      return false;
    }
    var x = -parseFloat(event.accelerationIncludingGravity.x);
    var y = -parseFloat(event.accelerationIncludingGravity.y);
    x = Math.round(x);
    y = Math.round(y);
    this.processAccelerationMovementX(x);
    this.processAccelerationMovementY(y);
  },
  processStop: function(){
    if (this.direction !== 'none'){
      this.direction = 'none';
      this.init();
    }
  },
  processAccelerationMovementX: function(x){        
    var turn = (x + 10)*5;               /* Converting from -10..10 to 0..100 */
    this.executeCommand('turn_' + turn);
  },
  processAccelerationMovementY: function(y){
    if (y < 0){
      if (this.direction !== 'bwd'){
        this.direction = 'bwd';
        this.executeCommand('move_bwd');
      };
    }
    else{
      if (this.direction !== 'fwd'){
        this.direction = 'fwd';
        this.executeCommand('move_fwd');
      };
    };
    var speed = Math.abs(y);
    var percent = parseInt(speed*10);   /* Converting from 0..10 to 0..100*/
    this.executeCommand('speed_' + percent);
  },
  executeCommand: function(command){
    command = this.filterCommands(command);
    this.ajaxHandler.sendRequest(command);
  },
  filterCommands: function(command){
    /*Since sending all gripmoves will flood the serve, we filter and send only the important ones*/
    /*We filter only speed and steer which are constantly changing and send only when the new value*/
    /*is not in the same gap as the previous one. The gap is defined by filterGap*/
    if (command.startsWith("speed_")){
      var newSpeed = parseInt(command.replace('speed_',''))
      newSpeed = Math.round(newSpeed/this.speedFilterGap)*this.speedFilterGap /* Converts in one of the gap boundaries*/
      if (newSpeed != this.lastSpeed){
        this.lastSpeed = newSpeed
        return "speed_" + newSpeed
      }
      else{
        return "none"
      }
    }
    else if (command.startsWith("turn_")){
      var newTurn = parseInt(command.replace('turn_',''))
      newTurn = Math.round(newTurn/this.turnFilterGap)*this.turnFilterGap /* Converts in one of the gap boundaries*/
      if (newTurn != this.lastTurn){
        this.lastTurn = newTurn
        return "turn_" + newTurn
      }
      else{
        return "none"
      }
    }
    else{
      return command;
    }
  },
  init: function(){
    this.ajaxHandler.sendRequest('move_stop');
    this.ajaxHandler.sendRequest('speed_0');
    this.ajaxHandler.sendRequest('turn_50');
  },
  vibrate: function(){
    window.navigator.vibrate(200);
  }
};