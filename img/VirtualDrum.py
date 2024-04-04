import cv2
import mediapipe as mp
import numpy as np
import pygame

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Initialize Pygame mixer for audio playback
pygame.mixer.init()

# Load drum sounds
snare_sound = pygame.mixer.Sound('snare.wav')
kick_sound = pygame.mixer.Sound('kick.wav')
hihat_sound = pygame.mixer.Sound('hihat.wav')

# Define drum pads (rectangles) coordinates and colors
drum_pads = {
    'snare': {'coords': (100, 400, 100, 100), 'color': (0, 255, 255)},  # x, y, width, height
    'kick': {'coords': (250, 400, 100, 100), 'color': (255, 0, 255)},
    'hihat': {'coords': (400, 400, 100, 100), 'color': (255, 255, 0)}
}

# Function to detect drum hits
def detect_drum_hits(hand_landmarks):
    for finger_tip in [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                       mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]:
        x = int(hand_landmarks.landmark[finger_tip].x * frame_width)
        y = int(hand_landmarks.landmark[finger_tip].y * frame_height)

        # Check for drum hits on each drum pad
        for pad_name, pad_info in drum_pads.items():
            pad_x, pad_y, pad_width, pad_height = pad_info['coords']
            if pad_x < x < pad_x + pad_width and pad_y < y < pad_y + pad_height:
                # Trigger corresponding drum sound
                if pad_name == 'snare':
                    snare_sound.play()
                elif pad_name == 'kick':
                    kick_sound.play()
                elif pad_name == 'hihat':
                    hihat_sound.play()

# Main function to capture webcam feed and play the virtual drum kit
def main():
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        global frame_height, frame_width
        frame_height, frame_width, _ = frame.shape

        # Process image with Mediapipe Hands
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Draw drum pads on frame
        for pad_name, pad_info in drum_pads.items():
            pad_x, pad_y, pad_width, pad_height = pad_info['coords']
            pad_color = pad_info['color']
            cv2.rectangle(frame, (pad_x, pad_y), (pad_x + pad_width, pad_y + pad_height), pad_color, -1)

        # Detect hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Detect drum hits
                detect_drum_hits(hand_landmarks)

        # Show frame
        cv2.imshow('Virtual Drum Kit', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
