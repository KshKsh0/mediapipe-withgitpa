import handtrackingModule as htm
import numpy as np 
import os 
import time 
import cv2

######
Wcam , Hcam=640 ,480
Himage , Wimage= 200, 200
folderPath='project 1/fingersImages'
overlayList=[]
Ptime=0
detector=htm.handDetector(detectionCon=.75) # u can edit this 
TipId=[4,8,12,16,20] # tip for every finger 
####
myList=os.listdir(folderPath)
for impath in myList:
    img=cv2.imread(f"{folderPath}/{impath}")
    overlayList.append(img)
    
    
cap=cv2.VideoCapture(0)
cap.set(3 ,Wcam)
cap.set(2, Hcam)

Ptime=0
detector=htm.handDetector(detectionCon=.75) # u can edit this 


while True :
    s, i=cap.read()
    i=detector.findHands(i)
    lmlist=detector.findPostition(i , draw=False)
    #to know which finger is up
    if len(lmlist)!= 0:
        fingers=[]
        totalFingers=0
        #thumb
        if lmlist[4][1]  < lmlist[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        #rest of the fingers
        for id in range(1,5):
                
            if lmlist[TipId[id]][2]  < lmlist[TipId[id ] - 2  ][2] :
                fingers.append(1)
            else:
                fingers.append(0)
        if fingers:     
            totalFingers=fingers.count(1)
            print(fingers)
    
        i[0:200 , 0:200]=cv2.resize(overlayList[totalFingers ] , (200,200)) 
    Ctime=time.time()
    fps=1 / ( Ctime - Ptime)
    Ptime=Ctime
    cv2.putText(i , f'FPS: {int(fps)}' , (400,100) , cv2.FONT_HERSHEY_COMPLEX_SMALL ,  2, (255,0,0) , 2)
    cv2.imshow('Image' , i)
    cv2.waitKey(1)