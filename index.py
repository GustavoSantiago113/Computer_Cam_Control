import cv2
import handDetection as hd
import mediapipe as mp
mp_hands = mp.solutions.hands

# Create a function to run when set to run
def main():
    
    # Opening the camera
    cap = cv2.VideoCapture(0)
    
    # Creating a variable to store the use the hand detector class
    hand_detector = hd.HandDetector()

    # While the camera is opened
    while cap.isOpened():
        
        # Stores the camera images in a variable
        success, image = cap.read()
        
        # Detecting hand and drawing lines
        image = hand_detector.findHands(image)
        
        # Display the frame with annotations
        cv2.imshow('Control Computer by hand movements', image)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    # Release the camera and close all OpenCV windows
    cap.release()

# Run the function
if __name__ == "__main__":
    main()