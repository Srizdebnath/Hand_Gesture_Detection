import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# Initialize the webcam
cap = cv2.VideoCapture(0)
# Set a standard resolution
cap.set(3, 1280)
cap.set(4, 720)

# Initialize the HandDetector with a higher confidence
detector = HandDetector(detectionCon=0.8, maxHands=1)

# A list of the landmark IDs for the TIPS of the fingers
tipIds = [4, 8, 12, 16, 20]

while True:
    # Read a frame from the webcam
    success, img = cap.read()
    if not success:
        break

    # Flip the image horizontally for a mirror effect
    img = cv2.flip(img, 1)

    # Find hands and their landmarks
    # --- FIX 1: Changed draw=False to draw=True ---
    hands, img = detector.findHands(img, draw=True)

    # A list to store landmark data if a hand is found
    lmList = []

    if hands:
        # Get the first hand detected
        hand1 = hands[0]
        lmList = hand1["lmList"]  # List of 21 Landmark points
        
        # We need at least the base landmarks to be present
        if len(lmList) != 0:
            fingers = [] # A list to store 0 or 1 for each finger

            # --- Thumb Logic ---
            # This logic checks if the thumb tip is horizontally past the knuckle.
            # It's a simple way to check if the thumb is "out".
            # It checks against the hand type to work for both left and right hands.
            if hand1['type'] == 'Right':
                if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else: # For Left Hand
                if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # --- Logic for the other 4 Fingers ---
            for id in range(1, 5):
                # Check if the fingertip is above the joint 2 landmarks down
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1) # Finger is up
                else:
                    fingers.append(0) # Finger is down
            
            # Count the total number of fingers up
            totalFingers = fingers.count(1)
            
            # --- Assign Commands based on Gestures ---
            gesture_text = ""
            if totalFingers == 0:
                gesture_text = "Fist / Stop"
            elif totalFingers == 1 and fingers[1] == 1: # Index finger
                gesture_text = "Point / Go"
            elif totalFingers == 2 and fingers[1] == 1 and fingers[2] == 1: # Index and Middle
                gesture_text = "Peace"
            elif totalFingers == 5:
                gesture_text = "Open Hand / Play"
            
            # Display the gesture text on the screen
            cv2.putText(img, gesture_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)


    # Display the final image
    cv2.imshow("Hand Gesture Recognition", img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()