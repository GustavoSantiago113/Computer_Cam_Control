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
    
    # Move the mouse
    def moveMouse(self, fingers, lmList):
        # Set the variables x1 and y1 as the coordinates of the tip of the index finger
        x1, y1 = lmList[8][1:]
        
        # If the index finger is up:
        if fingers[1] == 1:

            x3 = np.interp(x1, self.xp, self.fpx)
            y3 = np.interp(y1, self.yp, self.fpy)

            # Moving the cursor
            pyautogui.moveTo(self.screen_width - x3, y3)
    
    # Click
    def click(self, fingers, hand_detector):
        if fingers[1] == 1 and fingers[0] == 1:
                length = hand_detector.findDistance(5, 4)
                if length < 10:
                    pyautogui.click()