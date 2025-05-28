import cv2 as cv
import time as t 
import handDetection as hd
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

wcam , hcam = 640 , 480 

vid = cv.VideoCapture(0)
vid.set(3,wcam)
vid.set(4,hcam)
ptime = 0
detector = hd.handDetection(detectionCon=0.7)


device = AudioUtilities.GetSpeakers()
interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
minVol , maxVol , _ = volume.GetVolumeRange()
volBar = np.interp(int(volume.GetMasterVolumeLevel()) , [minVol , maxVol] , [400,150])
distance = 0 

while True :
    isTrue , frame = vid.read()
    if not isTrue :
        break
    
    frame = detector.findHands(frame , draw = False)
    lmlist = detector.findposition(frame , draw= False)
    if len(lmlist)>10 :
        x1 , y1 = lmlist[4][1] , lmlist[4][2]
        x2 , y2 = lmlist[8][1] , lmlist[8][2]
        distance = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
        c1,c2 = (x1+x2)//2 , (y1+y2)//2
        
        cv.circle(frame , (x1 , y1) , 10 , (0,0,255) , -1)
        cv.circle(frame , (x2 , y2) , 10 , (0,0,255) , -1)
        cv.line(frame , (x1,y1) , (x2,y2) , (255,0,255) , 2)
        cv.circle(frame , (c1,c2) , 10 , (255,0,0) , -1)
        
        if distance > 180 : 
            cv.circle(frame , (c1,c2) , 10 , (0,0,255) , -1)
        if distance < 40 :
            cv.circle(frame , (c1,c2) , 10 , (0,255,0) , -1)
            
        vol = np.interp(distance , [40 , 180] , [minVol , maxVol])
        volBar = np.interp(distance , [40 , 180] , [400,150])
        volume.SetMasterVolumeLevel(vol  , None)
        
    volper = np.interp(distance , [40 , 180] , [0,100])
    cv.rectangle(frame , (10,400) , (30,150) , (0,255,0) , 3)
    cv.rectangle(frame , (10,400) , (30 , int(volBar)) , (0,255,255) , -1)   
    cv.putText(frame , f"{int(volper)} %" , (10,450 ) ,  cv.FONT_HERSHEY_SIMPLEX , 1 , (255,0,0) , 2)     
    
    ctime = t.time()
    fps = 1/ (ctime - ptime)
    ptime = ctime
    
    cv.putText(frame , f"FPS : {int(fps)}"  , (10,25) , cv.FONT_HERSHEY_SIMPLEX , 1 , (255,0,255) , 2)
    cv.imshow('Video' , frame)
    
    cv.waitKey(10)
    if cv.waitKey(1) & 0xFF == ord('d'):
            break
        
vid.release()
cv.destroyAllWindows()