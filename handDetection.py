import mediapipe as mp
import cv2

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