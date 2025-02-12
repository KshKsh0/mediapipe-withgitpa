import cv2
import mediapipe as mp
import time
class handDetector():
    def __init__(self ,mode=False,
               maxHands=2,
               detectionCon=.5,
               trackCon=0.5,
               min_tracking_confidence=0.5):
        
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        self.mpHands=mp.solutions.hands
        self.hands = self.mpHands.Hands(
    static_image_mode=self.mode,
    max_num_hands=self.maxHands,
    min_detection_confidence=self.detectionCon,
    min_tracking_confidence=self.trackCon
)
        

        #for drawing
        self.mpDraw=mp.solutions.drawing_utils
        self.tip_id=[ 4 , 8 , 12 , 16 , 20]
    
    
    def findHands(self , i , draw=True):
        imgRGP=cv2.cvtColor(i , cv2.COLOR_BGR2RGB)
        self.res=self.hands.process(imgRGP)
        # print(res.multi_hand_landmarks)
        if draw :
            if self.res.multi_hand_landmarks:
                for handLms in self.res.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(i , handLms, self.mpHands.HAND_CONNECTIONS)
        return i
    
    
    def findPostition(self, img , handNo=0 , draw=True):
       
       lmlist=[]
       if self.res.multi_hand_landmarks:
         myHand=self.res.multi_hand_landmarks[handNo]
         for id , lm in enumerate(myHand.landmark):
                        # print(id ,lm )
                        h, w, c =img.shape
                        cx, cy =int(lm.x *w) , int(lm.y * h)
                        lmlist.append([id,cx,cy])
                        if draw:
                                cv2.circle(img, (cx ,cy) , 15 , (255,2,255) , cv2.FILLED )
       return lmlist

    
    def fingersUp(self, lmList):
        fingers = []
        # Thumb
        #for right hand only
        if self.lmList[self.tip_id[0]][1] < self.lmList[self.tip_id[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):
            if self.lmList[self.tip_id[id]][2] < self.lmList[self.tip_id[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

            # totalFingers = fingers.count(1)

        return fingers
    
def main():
        ptime=0
        ctime=0
        cap=cv2.VideoCapture(0)
        detector=handDetector()
        while True:
            s , i =cap.read()
            img=detector.findHands(i ,True)
            lmlist=detector.findPostition(i , handNo=0 , draw=True)
            if len(lmlist):
                print(lmlist[0])
            ctime=time.time()
            fps=1 /(ctime - ptime)
            ptime=ctime
            cv2.putText(i, str(int(fps)) , (10,70) , cv2.FONT_HERSHEY_COMPLEX , 2 , (255,0,255) , 2 )
            cv2.imshow('Image',i)
            cv2.waitKey(1)    
                                
if'__main__'==__name__:
    main()