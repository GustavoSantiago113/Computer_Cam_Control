import cv2
import handDetection as hd
import mouseControl as mc
import pyautogui

# Create a function to run when set to run
def main():
    # Opening the camera
    cap = cv2.VideoCapture(0)
    
    # Creating a variable to store the use the hand detector class
    hand_detector = hd.HandDetector()
    mouse_control = mc.MouseControl()

    # While the camera is opened
    while cap.isOpened():
        
        # Stores the camera images in a variable
        success, image = cap.read()
        
        # Detecting hand and drawing lines
        image = hand_detector.findHands(image)

        # Getting position of hand
        lmList = hand_detector.findPosition(image)

        # If a hand is detected and has position
        if len(lmList)!=0:

            # Check the fingers tips status
            fingers = hand_detector.fingersUp()

            # Move the mouse by using your left index finger up
            mouse_control.moveMouse(fingers, lmList)

            # Click by touching you thumb finger in your ring finger base
            mouse_control.click(fingers, hand_detector)

        # Display the frame with annotations
        cv2.imshow('Control Computer by hand movements', cv2.flip(image, 1))

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    # Release the camera and close all OpenCV windows
    cap.release()

# Run the function
if __name__ == "__main__":
    main()