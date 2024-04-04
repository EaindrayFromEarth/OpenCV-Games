import cv2
import numpy as np
import random

# Function to draw fruits
def draw_fruit(image, fruit):
    image[fruit['y']:fruit['y']+fruit['h'], fruit['x']:fruit['x']+fruit['w']] = fruit['color']

# Function to update fruit positions
def update_fruits(fruits, speed):
    for fruit in fruits:
        fruit['y'] += speed
        if fruit['y'] > SCREEN_HEIGHT:
            fruit['y'] = -fruit['h']
            fruit['x'] = random.randint(0, SCREEN_WIDTH - fruit['w'])

# Function to detect fruit collisions with index finger
def detect_collisions(fruits, index_finger):
    for fruit in fruits:
        if (index_finger[0] > fruit['x'] and index_finger[0] < fruit['x'] + fruit['w'] and
            index_finger[1] > fruit['y'] and index_finger[1] < fruit['y'] + fruit['h']):
            return True, fruit
    return False, None

# Function to display score
def display_score(image, score):
    cv2.putText(image, "Score: " + str(score), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Main function to run the game
def main():
    cap = cv2.VideoCapture(0)

    fruits = []
    for _ in range(NUM_FRUITS):
        fruit = {'x': random.randint(0, SCREEN_WIDTH - FRUIT_SIZE),
                 'y': random.randint(0, SCREEN_HEIGHT - FRUIT_SIZE),
                 'w': FRUIT_SIZE, 'h': FRUIT_SIZE,
                 'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))}
        fruits.append(fruit)

    score = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Update and draw fruits
        update_fruits(fruits, FRUIT_SPEED)
        for fruit in fruits:
            draw_fruit(frame, fruit)

        # Detect hand and index finger (simulated)
        index_finger = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

        # Detect collisions
        collision, sliced_fruit = detect_collisions(fruits, index_finger)
        if collision:
            score += 1
            fruits.remove(sliced_fruit)

        # Display score
        display_score(frame, score)

        cv2.imshow('Fruit Cutting Game', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    NUM_FRUITS = 20
    FRUIT_SIZE = 50
    FRUIT_SPEED = 5

    main()
