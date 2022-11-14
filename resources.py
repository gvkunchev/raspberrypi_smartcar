#!/usr/bin/python

# Resources are stored here to prevent multiple lines in other files

cameraButtons = [
 {
   'oncommand':'cam_up',
   'offcommand':'none',
   'key':'87',
   'text':'Up <br/> (W)',
   'break': True
 },
 {
   'oncommand':'cam_left',
   'offcommand':'none',
   'key':'65',
   'text':'Left <br/> (A)',
   'break': False
 },
 {
   'oncommand':'cam_home',
   'offcommand':'none',
   'key':'83',
   'text':'Home <br/> (S)',
   'break': False
 },
 {
   'oncommand':'cam_right',
   'offcommand':'none',
   'key':'68',
   'text':'Right <br/> (D)',
   'break': True
 },
 {
   'oncommand':'cam_down',
   'offcommand':'none',
   'key':'88',
   'text':'Down <br/> (X)',
   'break': False
 },
]

movementButtons = [
 {
   'oncommand':'move_fwd',
   'offcommand':'move_stop',
   'key':'38',
   'text':'Forward <br/> (Arrow up)',
   'break': True
 },
 {
   'oncommand':'steer_left',
   'offcommand':'steer_home',
   'key':'37',
   'text':'Left <br/> (Arrow left)',
   'break': False
 },
 {
   'oncommand':'move_stop',
   'offcommand':'none',
   'key':'32',
   'text':'Stop <br/> (Space)',
   'break': False
 },
 {
   'oncommand':'steer_right',
   'offcommand':'steer_home',
   'key':'39',
   'text':'Right <br/> (Arrow right)',
   'break': True
 },
 {
   'oncommand':'move_bwd',
   'offcommand':'move_stop',
   'key':'40',
   'text':'Backward <br/> (Arrow down)',
   'break': False
 },
]