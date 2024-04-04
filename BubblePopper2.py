import cv2
import mediapipe as mp
import numpy as np
import random

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Initialize variables
score = 0
fruits = []
fruit_speed = 5

# Function to detect collisions between two rectangles
def is_collision(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    if (x1 < x2 + w2 and x1 + w1 > x2 and
            y1 < y2 + h2 and y1 + h1 > y2):
        return True
    return False

# Main function to capture webcam feed and play the game
def main():
    global score  # Declare score as a global variable to be able to modify it inside the function
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_height, frame_width, _ = frame.shape

        # Generate fruits
        if len(fruits) < 3:
            fruit_type = random.choice(['apple', 'banana', 'orange'])
            fruit_x = random.randint(0, frame_width - 50)
            fruit_y = frame_height
            fruits.append({'type': fruit_type, 'x': fruit_x, 'y': fruit_y})

        # Move and draw fruits
        for fruit in fruits:
            fruit['y'] -= fruit_speed
            if fruit['y'] < 0:
                fruits.remove(fruit)
                continue
            if fruit['type'] == 'apple':
                cv2.circle(frame, (fruit['x'], fruit['y']), 20, (0, 255, 0), -1)
            elif fruit['type'] == 'banana':
                cv2.rectangle(frame, (fruit['x'], fruit['y']), (fruit['x'] + 40, fruit['y'] + 100), (255, 255, 0), -1)
            elif fruit['type'] == 'orange':
                cv2.circle(frame, (fruit['x'], fruit['y']), 20, (0, 165, 255), -1)

        # Process image with Mediapipe Hands
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Detect hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_finger_tip_x = int(index_finger_tip.x * frame_width)
                index_finger_tip_y = int(index_finger_tip.y * frame_height)

                # Check for collisions with fruits
                for fruit in fruits:
                    if fruit['type'] == 'apple':
                        fruit_rect = (fruit['x'] - 20, fruit['y'] - 20, 40, 40)
                    elif fruit['type'] == 'banana':
                        fruit_rect = (fruit['x'], fruit['y'], 40, 100)
                    elif fruit['type'] == 'orange':
                        fruit_rect = (fruit['x'] - 20, fruit['y'] - 20, 40, 40)
                    if is_collision((index_finger_tip_x, index_finger_tip_y, 5, 5), fruit_rect):
                        score += 1
                        fruits.remove(fruit)

                # Draw index finger tip
                cv2.circle(frame, (index_finger_tip_x, index_finger_tip_y), 5, (255, 0, 0), -1)

        # Display score
        cv2.putText(frame, 'Score: {}'.format(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Show frame
        cv2.imshow('Fruit Cutting Game', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
