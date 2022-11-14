import os
from flask import Flask, render_template, request, Response, url_for
from resources import cameraButtons, movementButtons
from garage.components.hardware.Camera import Camera
from garage.Car import Car
from garage.Driver import Driver

def dated_url_for(endpoint, **values):
  "Updates the url building function so that it automatically serves the latest version of the file"
  if endpoint == 'static':
    filename = values.get('filename', None)
    if filename:
      file_path = os.path.join(app.root_path,
                   endpoint, filename)
      values['q'] = int(os.stat(file_path).st_mtime)
  return url_for(endpoint, **values)
  
def gen(camera):
  "Keep on sending new frames to the client"
  while True:
    frame = camera.getFrame()
    yield (b'--frame\r\n'
       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Set up an app
app    = Flask(__name__)
# Init a Car and a Driver to operate it
car    = Car()
driver = Driver(car)

# Implement the custom url building function defined above
@app.context_processor
def override_url_for():
  return dict(url_for=dated_url_for)

# Default route, loading the interface
@app.route('/')
def index():
  ratio      = request.args.get('video', '0.3', type=float)
  blackwhite = request.args.get('bw', '1', type=str)
  return render_template('index.html',
                         cameraButtons   = cameraButtons,
                         movementButtons = movementButtons,
                         ratio           = ratio,
                         blackwhite      = blackwhite)

# Route for the img tag that shows the video frames
@app.route('/videoFeed')
def videoFeed():
  ratio      = request.args.get('ratio', '1.0', type=float)
  blackwhite = request.args.get('blackwhite', '0', type=int)
  return Response(gen(Camera(ratio=ratio, blackwhite=blackwhite)),
                  mimetype='multipart/x-mixed-replace; boundary=frame')

# Route for remove command listening
@app.route('/remoteControl')
def remoteControl():
  command = request.args.get('command', 'none', type=str)
  driver.executeCommand(command)
  return "Received the following command: " + command

app.run(host='0.0.0.0', debug=True, threaded=True)
