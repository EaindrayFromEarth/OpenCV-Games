import cv2
import numpy as np
import pygame

# Initialize Pygame mixer for audio playback
pygame.mixer.init()

# Load sound effects
player_x_sound = pygame.mixer.Sound('hihat.wav')
player_o_sound = pygame.mixer.Sound('kick.wav')
win_sound = pygame.mixer.Sound('win_sound.wav')
draw_sound = pygame.mixer.Sound('draw_sound.wav')

# Initialize game variables
board = np.zeros((3, 3), dtype=int)  # Tic Tac Toe board
turn = 1  # 1 for Player X, -1 for Player O
winner = None
game_over = False

# Function to check if there is a winner
def check_winner():
    global winner, game_over
    # Check rows
    for row in board:
        if all(row == 1):
            winner = 'Player X'
            game_over = True
            return True
        elif all(row == -1):
            winner = 'Player O'
            game_over = True
            return True
    # Check columns
    for col in board.T:
        if all(col == 1):
            winner = 'Player X'
            game_over = True
            return True
        elif all(col == -1):
            winner = 'Player O'
            game_over = True
            return True
    # Check diagonals
    if all(np.diag(board) == 1) or all(np.diag(np.fliplr(board)) == 1):
        winner = 'Player X'
        game_over = True
        return True
    elif all(np.diag(board) == -1) or all(np.diag(np.fliplr(board)) == -1):
        winner = 'Player O'
        game_over = True
        return True
    # Check for draw
    if not any(0 in row for row in board):
        winner = 'Draw'
        game_over = True
        return True
    return False

# Function to handle mouse click events
def handle_click(event, x, y, flags, param):
    global turn, game_over
    if event == cv2.EVENT_LBUTTONDOWN and not game_over:
        row = y // (frame_height // 3)
        col = x // (frame_width // 3)
        if board[row, col] == 0:
            board[row, col] = turn
            if turn == 1:
                player_x_sound.play()
                turn = -1
            else:
                player_o_sound.play()
                turn = 1
            if check_winner():
                if winner == 'Draw':
                    draw_sound.play()
                else:
                    win_sound.play()

# Initialize game window
frame_width, frame_height = 300, 300
cv2.namedWindow('Tic Tac Toe')
cv2.setMouseCallback('Tic Tac Toe', handle_click)

# Main game loop
while True:
    frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

    # Draw Tic Tac Toe grid
    cv2.line(frame, (frame_width // 3, 0), (frame_width // 3, frame_height), (255, 255, 255), 2)
    cv2.line(frame, (2 * frame_width // 3, 0), (2 * frame_width // 3, frame_height), (255, 255, 255), 2)
    cv2.line(frame, (0, frame_height // 3), (frame_width, frame_height // 3), (255, 255, 255), 2)
    cv2.line(frame, (0, 2 * frame_height // 3), (frame_width, 2 * frame_height // 3), (255, 255, 255), 2)

    # Draw X's and O's
    for i in range(3):
        for j in range(3):
            if board[i, j] == 1:
                cv2.putText(frame, 'X', (j * (frame_width // 3) + 30, i * (frame_height // 3) + 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
            elif board[i, j] == -1:
                cv2.putText(frame, 'O', (j * (frame_width // 3) + 30, i * (frame_height // 3) + 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    # Display winner or draw message
    if game_over:
        cv2.putText(frame, f'Winner: {winner}', (30, frame_height - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Tic Tac Toe', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
