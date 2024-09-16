'''
    To run multiple programs simultaneously through multi-procesing

'''

from multiprocessing import Process, Manager
from PyQt5.QtWidgets import QApplication
import time
import cv2
from camera import Camera 
from openVideo import Video
# from mainUI import Window
import sys
from detection import Model
class runApplication:

    def runCamera(param):
        cam = Camera()
        cam.toDisplay = False # change True if nahan ka mag display
        cam.publish(param)
    
    def runVideo(param):
        cam = Video() #Camera()
        cam.toDisplay = True # change True if nahan ka mag display
        cam.publish(param)

    def closeCamera(param):
        print("Opening Camera.")
        time.sleep(60)
        print("Closing Camera.")
        param['camStatus'].value = False

    def runModel(param):
        while param['videoFrame'].value is None:
            continue # wait while frame is available
        mod = Model() #gi call niya ang from 

        while(param['camStatus'].value):
            mod.receiverFrame(param) #sudlan ug param na argument, ang sulod ni param kay camstatus ug frame

if __name__ == '__main__':
    ra =runApplication
    param = {}

    param['camStatus'] = Manager().Value('camStatus', False)
    param['frame'] = Manager().Value('frame', None)
    param['videoFrame'] = Manager().Value('frame', None)
    

    p = [
        # Process(target=ra.runCamera, args=(param,)),
        Process(target=ra.runModel, args=(param,)), #class ayha ang funtion
        Process(target=ra.runVideo, args=(param,)), #class ayha ang funtion
        # Process(target=closeCamera, args=(param,)),
    ]

    for process in p:
        process.start()

    for process in p:
        process.join()
