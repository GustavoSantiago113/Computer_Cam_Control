import mediapipe as mp
import cv2
import math

# Creating the class to detect and draw the annotations in the hands
class HandDetector():
    
    # Initializing the class, with the needed variables
    def __init__(self, model_complexity = 0, min_detection_confidence = 0.5, min_tracking_confidence = 0.5):
        
        self.model_complexity = model_complexity
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands()

        # Ids of the tip of the fingers
        self.tipIds = [4, 8, 12, 16, 20]
        
    # Creating the function to return the hands location
    def findHands(self, image):
        
        # Dont allow writing in the image yet
        image.flags.writeable = False

        # Convert the image to RGB
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Apply the model in the image
        self.results = self.hands.process(imageRGB)

        # Allow to make draws in the image
        image.flags.writeable = True
        
        # If there are any hand detections in the image, draw them
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())
                
        return image
    
    def findPosition(self, img, handNo=0):   # Fetches the position of a hand
        
        # Creating empty lists to store position
        xList = []
        yList = []
        self.lmList = []

        # If a hand is detected:
        if self.results.multi_hand_landmarks:
            # Gets the information of a hand
            myHand = self.results.multi_hand_landmarks[handNo]
            # For each information, get and store the information
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])

        return self.lmList
    
    # Check if index finger is up
    def fingersUp(self):    
        fingers = [] 
        
        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):

            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
    
    # Finds distance between two fingers
    def findDistance(self, p1, p2):   
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        length = math.hypot(x2 - x1, y2 - y1)

        return length