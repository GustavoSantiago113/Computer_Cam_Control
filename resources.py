import pyautogui
import numpy as np
import mediapipe as mp
import cv2
import math
import time

# Creating the class to detect and draw the annotations in the hands
class HandDetector():
    
    # Initializing the class, with the needed variables
    def __init__(self, model_complexity = 0, min_detection_confidence = 0.75, min_tracking_confidence = 0.75):
        
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
    
    # Fetches the position of a hand
    def findPosition(self, img, handNo=0, handType = None):
        
        # Creating empty lists to store position
        xList = []
        yList = []
        self.lmList = []

        # If a hand is detected:
        if self.results.multi_hand_landmarks:
            # For each hand detected
            for hand in self.results.multi_handedness:
                # If the hand is the same as selected previously:
                if hand.classification[0].label == handType:
                    # Gets the information of the hand
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
    def fingersUp(self, lmList, hand):    
        fingers = [] 
        
        # Right hand
        if hand == "Right":
            # Thumb
            if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0] - 1][1]:
                fingers.append(0)
            else:
                fingers.append(1)
        if hand == "Left":
            # Thumb
            if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Fingers
        for id in range(1, 5):

            if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
    
    # Finds distance between two fingers
    def findDistance(self, p1, p2, lmList):

        x1, y1 = lmList[p1][1:]
        x2, y2 = lmList[p2][1:]

        length = math.hypot(x2 - x1, y2 - y1)
        return length
    

# Creating a class to control the mouse - movement and clicking
class MouseControl():

    def __init__(self, width = 640, height=480, frameR = 100 ):
        
        self.screen_width, self.screen_height = pyautogui.size() # Screen width and height
        self.width = width # Width of Camera
        self.height = height # Height of Camera
        self.frameR = frameR # Frame rate

        # Parameters for the coordinates interpolation
        self.xp = [self.frameR, self.width-self.frameR]
        self.fpx = [0, self.screen_width]

        # Parameters for the coordinates interpolation
        self.yp = [self.frameR , self.height-self.frameR]
        self.fpy = [0, self.screen_height]

    # Move the mouse
    def moveMouse(self, fingers, lmList):
        
        # Set the variables x1 and y1 as the coordinates of the base of the middle finger
        x1, y1 = lmList[9][1:]
        
        self.x3 = np.interp(x1, self.xp, self.fpx)
        self.y3 = np.interp(y1, self.yp, self.fpy)

        # If the index finger is up:
        if fingers[1] == 1:
            
            # Moving the cursor
            pyautogui.moveTo(self.screen_width - self.x3, self.y3)
    
    # Click
    def click(self, fingers):
        
        cooldown_time = 1
        last_toggle_time = 0
        current_time = time.time()

        if (current_time - last_toggle_time) > cooldown_time:

            if fingers[1] == 1: 
                
                pyautogui.mouseUp(button = "left")

                # Click with the left button by touching your thumb finger in your ring finger base
                if fingers[2] == 1:
                    pyautogui.click()
                    last_toggle_time = current_time

                # Double click with the left button by putting up index and middle fingers
                if fingers[2] == 1 and fingers[3] == 1:
                    pyautogui.click(clicks=2)
                    last_toggle_time = current_time

                if fingers[4] == 1:
                    # Right click by putting up the index and pinky fingers
                    pyautogui.click(button = "right")
                    last_toggle_time = current_time
    
    # Drag
    def drag(self, fingers):

        cooldown_time = 1
        last_toggle_time = 0
        current_time = time.time()

        if (current_time - last_toggle_time) > cooldown_time:

            # Keep the hand closed to click and drag
            if all(element == 0 for element in fingers):
                pyautogui.mouseDown(button = "left")
                pyautogui.moveTo(self.screen_width - self.x3, self.y3)
                last_toggle_time = current_time

# Class to control the volume
class VolumeControl():
    def __init__(self) -> None:
        pass

    # Defining the function to perform it
    def volume(self, fingers, hand_detector, lmList):
       
        # If all the fingers are up:
        if all(element == 1 for element in fingers):

            # Get the distance between index and thumb tips
            length = hand_detector.findDistance(4, 8, lmList)
            
            # Change the volume by the distance
            if length > 50:
                pyautogui.press("volumeup")
            else:
                pyautogui.press("volumedown")

# Class to use keyboards
class KeyboardShortcuts():
    def __init__(self) -> None:
        pass

    # Defining the function to do it
    def shortcuts(self, fingers):

        cooldown_time = 1
        last_toggle_time = 0
        current_time = time.time()

        if (current_time - last_toggle_time) > cooldown_time:
            # If only the thumb is up, use left arrow:
            if fingers[0] == 1 and all(finger ==0 for finger in fingers[1:]):
                pyautogui.press("left")
                last_toggle_time = current_time
                
            # If only the pinky is up, use right arrow:
            if all(finger ==0 for finger in fingers[:4]) and fingers[4] == 1:
                pyautogui.press("right")
                last_toggle_time = current_time
            
            # If only the index finger is up, use up arrow:
            if fingers[0] == 0 and fingers[1] == 1 and all(finger ==0 for finger in fingers[2:]):
                pyautogui.press("up")
                last_toggle_time = current_time
            
            # If both index and middle fingers are up, use down arrow:
            if fingers[0] == 0 and all(finger == 1 for finger in fingers[1:3]) and all(finger == 0 for finger in fingers[3:]):
                pyautogui.press("down")
                last_toggle_time = current_time
            
            # If both thumb and index fingers are up, use Esc:
            if all(finger == 1 for finger in fingers[0:2]) and all(finger == 0 for finger in fingers[2:]):
                pyautogui.press("esc")
                last_toggle_time = current_time
            
            # If both thumb and pinky fingers are up, use enter:
            if fingers[0] == 1 and all(finger == 0 for finger in fingers[1:4]) and fingers[4] == 1:
                pyautogui.press("space")
                last_toggle_time = current_time
            
            # If both index and pinky fingers are up, open keyboard:
            if fingers[0] == 0 and fingers[1] == 1 and all(finger == 0 for finger in fingers[2:4]) and fingers[4] == 1:
                pyautogui.hotkey('ctrl', 'win', 'o')
                last_toggle_time = current_time

# Class to zoom in and out
class Zoom():

    def __init__(self) -> None:
        pass

    def zoomIn_zoomOut(self, fingers, fingersR):

        # If both thumb fingers are up:
        if fingers[0] == 1 and fingersR[0] == 0 and all(finger == 0 for finger in fingers[1:]) and all(finger == 0 for finger in fingersR[1:]):
            # Zoom In
            pyautogui.hotkey('ctrl', '+')
        
        # If both index fingers are up:
        if fingers[0] == 0 and fingersR[0] == 1 and fingers[1] == 1 and fingersR[1] == 1 and all(finger == 0 for finger in fingers[2:]) and all(finger == 0 for finger in fingersR[2:]):
            # Zoom In
            pyautogui.hotkey('ctrl', '-')

# Class to start-stop
class StartStop():

    def __init__(self, cooldown_time=2.0):
        self.last_toggle_time = 0
        self.cooldown_time = cooldown_time

    def start(self, start, fingers, fingersR):

        # Get the current time
        current_time = time.time()

        # If all the fingers are up:
        if (current_time - self.last_toggle_time) > self.cooldown_time:
            if fingers[0] == 0 and fingersR[0] == 1 and all(finger == 1 for finger in fingers[1:]) and all(finger == 1 for finger in fingersR[1:]):
                start = not start
                self.last_toggle_time = current_time
                print(start)
        
        return start
        