import cv2
import resources as mg

# Create a function to run when set to run
def main():
    # Opening the camera
    cap = cv2.VideoCapture(0)
    
    # Creating a variable to store the use the classes
    hand_detector = mg.HandDetector()
    mouse_control = mg.MouseControl()
    volume_control = mg.VolumeControl()
    keyboard_control = mg.KeyboardShortcuts()
    zoom_control = mg.Zoom()

    # While the camera is opened
    while cap.isOpened():
        
        # Stores the camera images in a variable
        success, image = cap.read()
        
        # Detecting hand and drawing lines
        image = hand_detector.findHands(image)

        # Getting position of left hand
        lmList = hand_detector.findPosition(image, handType = "Right")

        # Getting position of right hand
        lmListR = hand_detector.findPosition(image, handType = "Left")

        ### LOGICAL FOR LEFT HAND ###

        # If a hand is detected and has position
        if len(lmList)!=0 and len(lmListR)==0:

            """ # Check the fingers tips status
            fingers = hand_detector.fingersUp(lmList, "Right")

            # Move the mouse by using your left index finger up
            mouse_control.moveMouse(fingers, lmList)

            # Click
            mouse_control.click(fingers, hand_detector)

            # Drag
            mouse_control.drag(fingers) """
        
        ### LOGICAL FOR RIGHT HAND ###

        # If a hand is detected and has position
        if len(lmListR)!=0 and len(lmList)==0:
            print("Direita")
            """ # Check the fingers tips status
            fingersR = hand_detector.fingersUp(lmListR, "Left")
            
            # Change the volume
            volume_control.volume(fingersR, hand_detector)

            # Use keyboard shortcuts
            keyboard_control.shortcuts(fingersR) """

        ### LOGICAL FOR BOTH HANDS ###
        
        # If both hands are in the screen
        if len(lmListR)!=0 and len(lmList)!=0:
            print("Ambas")
            """ # Getting fingers values
            fingers = hand_detector.fingersUp(lmList, "Right")
            fingersR = hand_detector.fingersUp(lmListR, "Left")

            # Perform zoom in and out
            zoom_control.zoomIn_zoomOut(fingers, fingersR) """

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