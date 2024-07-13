import pyautogui
import numpy as np

# Creating a class to control the mouse - movement and clicking
class MouseControl():

    def __init__(self, width = 640, height = 480, frameR = 100 ):
        
        self.screen_width, self.screen_height = pyautogui.size() # Screen width and height
        self.width = width # Width of Camera
        self.height = height # Height of Camera
        self.frameR = frameR # Frame rate
        
        # Parameters for the coordinates interpolation
        self.xp = [frameR, width-frameR]
        self.fpx = [0, self.screen_width]

        # Parameters for the coordinates interpolation
        self.yp = [frameR , height-frameR]
        self.fpy = [0, self.screen_height]

        # Check if is dragging
        self.dragging = False
    
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
    def click(self, fingers, hand_detector):
        if fingers[1] == 1:
            length = hand_detector.findDistance(5, 4)
            pyautogui.mouseUp(button = "left")

            # Click with the left button by touching your thumb finger in your ring finger base
            if length < 12:
                pyautogui.click()

            # Double click with the left button by putting up index and middle fingers
            if fingers[2] == 1:
                pyautogui.click(clicks=2)

        if fingers[1] == 1 and fingers[4] == 1:
            # Right click by putting up the index and pinky fingers
            pyautogui.click(button = "right")
    
    # Drag
    def drag(self, fingers):
        # Keep the hand closed to click and drag
        if all(element == 0 for element in fingers):
            pyautogui.mouseDown(button = "left")
            pyautogui.moveTo(self.screen_width - self.x3, self.y3)

        