#https://www.hackster.io/ruchir1674/video-streaming-on-flask-server-using-rpi-ef3d75-----------------------#

import time
import io
import threading
try:
    import picamera
    import picamera.array
except:
    pass
import cv2
import numpy as np
import logging
import argparse
import imutils
import glob


class CameraInterface(object):

    def __init__(self, logger=logging.getLogger(), resolution = (320,240), framerate=32):
        self.frame = None  # current frame is stored here by background thread
        self.logger=logger
        self.camera = picamera.PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.camera.hflip = True; self.camera.vflip = True #not sure what this does
        self.rawCapture = io.BytesIO()
        self.stream = None
        self.thread = None
        self.stopped = False
        return

    def start(self):
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.log("CAMERA INTERFACE: Started Camera Thread")
        return
        
    def log(self, message):
        self.logger.info(message)
        return

    def get_frame(self):
        return self.frame

    def stop(self):
        self.stopped = True
        return

    # Thread reads frames from the stream
    def update(self):
        self.camera.start_preview()
        time.sleep(2)
        self.stream = self.camera.capture_continuous(self.rawCapture, 'jpeg', use_video_port=True)
        for f in self.stream:
            self.rawCapture.seek(0)
            self.frame = self.rawCapture.read()
            self.rawCapture.truncate(0)
            self.rawCapture.seek(0)

            # stop the thread
            if self.stopped:
                self.camera.stop_preview()
                time.sleep(2)
                self.rawCapture.close()
                self.stream.close()
                self.camera.close()
                self.log("CAMERA INTERFACE: Exiting Camera Thread")
                return
        return
    
    #detect if there is a colour in the image
    def get_camera_colour(self):
        if not self.frame: #hasnt read a frame from camera
            return "camera is not running yet"
        img = cv2.imdecode(np.fromstring(self.frame, dtype=np.uint8), 1)
        # set red range
        Redlowcolor = (50,50,150)
        Redhighcolor = (150,150,255)
        Bluelowcolor = (150,50,50)
        Bluehighcolor = (255,150,150)
        greenlowcolor = (50,150,50)
        greenhighcolor = (150,255,150)

        # threshold
        Redthresh = cv2.inRange(img, Redlowcolor, Redhighcolor)
        Bluethresh = cv2.inRange(img, Bluelowcolor, Bluehighcolor)
        greenthresh = cv2.inRange(img, greenlowcolor, greenhighcolor)

        cv2.imwrite("threshold.jpg", Redthresh)
        cv2.imwrite("threshold.jpg", Bluethresh)
        cv2.imwrite("threshold.jpg", greenthresh)

        Redcount = np.sum(np.nonzero(Redthresh))
        Bluecount = np.sum(np.nonzero(Bluethresh))
        greencount = np.sum(np.nonzero(greenthresh))
        
        if Redcount>Bluecount and Redcount>greencount:
            self.log("mostly red")
        if Bluecount>Redcount and Bluecount>greencount:
            self.log("mostly blue")
        if greencount>Redcount and greencount>Bluecount:
            self.log("mostly green")
        return


