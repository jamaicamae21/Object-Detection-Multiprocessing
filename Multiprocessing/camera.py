import cv2
'''
    To store frame from the live stream camera to the memory 
'''

import threading
import time


class Camera:
    # output attribute
    frame = None

    # miscellaneous attribute
    cam = None
    cameraStatus = False
    toDisplay = True

    # Required functions

    def publish(self, param=None): #if walay value na ma receive ang param kay automatic na ma None
        self.openCamera(param=param)
        self.setCurrentFrame(param=param)

    def openCamera(self, param=None):
        if not self.isCameraOpen(param):
            # rtsp_url = "rtsp://192.168.144.25:8554/main.264"
            self.cam = cv2.VideoCapture(0)
            self.cameraStatus = True
            if param is not None:
                param['camStatus'].value = True

    def isCameraOpen(self, param=None):
        return self.cameraStatus if param is None else param['camStatus'].value

    def setCurrentFrame(self, param=None):
        while self.isCameraOpen(param):
            ret, frame = self.cam.read()
            self.frames = frame
            if param is not None:
                # need this to publish topic frame
                param['frame'].value = frame
            if self.toDisplay:
                cv2.imshow('a', frame)
                cv2.waitKey(1)
        self.cam.release()
        cv2.destroyAllWindows()

    def closeCamera(self):
        self.cameraStatus = False

    def getFrame(self):
        return self.frames

    # Miscellaneous functions

    def cameraTest(self):
        print("open")
        time.sleep(5)
        print("close")
        self.closeCamera()


if __name__ == "__main__":
    a = Camera()

    t = threading.Thread(target=a.publish)
    t1 = threading.Thread(target=a.cameraTest)

    t.start()
    t1.start()
