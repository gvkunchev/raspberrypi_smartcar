"use strict";

$(document).ready(function(){
  var ajaxHandler     = new AjaxHandler("/remoteControl", "GET");
  var drivingChoice   = new DrivingChoice($('#driving_choice'), ajaxHandler);
  var speedSlider     = new SpeedSlider($('#speed_slider_wrapper'), ajaxHandler);
  var drivingJoystick = new DrivingJoystick($('#direction_joystick'), ajaxHandler);
  var accelerometer   = new Accelerometer($('#phone_accelerometer'), ajaxHandler);
  $('.button-controller').each(function(i,e){
    var carButton = new CarButton(e, ajaxHandler);
  });
});