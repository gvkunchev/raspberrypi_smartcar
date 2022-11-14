#!/usr/bin/python
import cv2

class Camera(object):
  "Object for accessing the first (default) camera with specific ratio and flag for converting to black&white"

  # These are the default values for width and height of the video frames
  defaultWidth  = 640
  defaultHeight = 480

  def __init__(self, ratio=1.0, blackwhite=False):
    # param: ratio      - float (A coefficient to resize the image width/height)
    # param: blackwhite - bool  (Flag for convertin to black&white)
    assert type(ratio) is float, "The ratio must be a float number"
    self.video      = cv2.VideoCapture(0)
    self.blackwhite = bool(blackwhite)
    self.video.set(3, int(self.defaultWidth*ratio))   # Video width
    self.video.set(4, int(self.defaultHeight*ratio))  # Video Height
  
  def __del__(self):
    self.video.release()
    
  def _convertImage(self, image):
    # param: image - object (The raw image that need to be converted to black&white based on the settings)
    if self.blackwhite:
      return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image
  
  def getFrame(self):
    success, image = self.video.read()
    if not success:
      raise Exception("Cannot read from video camera")
    image     = self._convertImage(image)
    ret, jpeg = cv2.imencode('.jpg', image)
    return jpeg.tostring()

if __name__ == "__main__":
  pass