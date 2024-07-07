import cv2
import mediapipe as mp
import pygame
import sys
import matplotlib.pyplot as plt

# Initialize Mediapipe Hand Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load music and sounds
pygame.mixer.music.load("background_music.mp3")
hit_sound = pygame.mixer.Sound("hit_sound.wav")
wall_sound = pygame.mixer.Sound("wall_sound.wav")

# Play background music
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Finger-Controlled Paddle Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont("comicsansms", 30)
level_font = pygame.font.SysFont("comicsansms", 40, bold=True)

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10

# Ball dimensions
BALL_RADIUS = 8

# Paddle and ball initial positions
paddle_x, paddle_y = WIDTH // 2, HEIGHT - 30
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = 4, -4

# Game variables
score = 0
level = 1
score_threshold = 5

# Button dimensions and positions
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50
increase_button = pygame.Rect(WIDTH - 220, HEIGHT - 70, BUTTON_WIDTH, BUTTON_HEIGHT)
decrease_button = pygame.Rect(WIDTH - 120, HEIGHT - 70, BUTTON_WIDTH, BUTTON_HEIGHT)

# Capture Video
cap = cv2.VideoCapture(0)

def detect_hand_position(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)
    hand_position = None
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * WIDTH)
            y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * HEIGHT)
            hand_position = (x, y)
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    return hand_position, image

plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hand_position, frame = detect_hand_position(frame)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            sys.exit()

    if hand_position:
        paddle_x = hand_position[0] - PADDLE_WIDTH // 2

        # Check if hand is over the increase button
        if increase_button.collidepoint(hand_position):
            ball_dx *= 1.1
            ball_dy *= 1.1

        # Check if hand is over the decrease button
        if decrease_button.collidepoint(hand_position):
            ball_dx *= 0.9
            ball_dy *= 0.9

    screen.fill(BLACK)
    
    # Draw paddle
    pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    
    # Move and draw ball
    ball_x += ball_dx
    ball_y += ball_dy
    pygame.draw.circle(screen, GREEN, (ball_x, ball_y), BALL_RADIUS)
    
    # Ball collision with walls
    if ball_x <= BALL_RADIUS or ball_x >= WIDTH - BALL_RADIUS:
        ball_dx = -ball_dx
        wall_sound.play()
    if ball_y <= BALL_RADIUS:
        ball_dy = -ball_dy
        wall_sound.play()
    if ball_y >= HEIGHT - BALL_RADIUS:
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_dy = -ball_dy
        score = 0  # Reset score if ball hits the bottom
    
    # Ball collision with paddle
    if paddle_y <= ball_y + BALL_RADIUS <= paddle_y + PADDLE_HEIGHT and \
       paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH:
        ball_dy = -ball_dy
        score += 1
        hit_sound.play()
        if score % score_threshold == 0:
            level += 1
            ball_dx *= 1.1
            ball_dy *= 1.1
    
    # # Draw buttons
    # pygame.draw.rect(screen, RED, increase_button)
    # pygame.draw.rect(screen, RED, decrease_button)
    # increase_text = font.render("Speed +", True, WHITE)
    # decrease_text = font.render("Speed -", True, WHITE)
    # screen.blit(increase_text, (increase_button.x + 10, increase_button.y + 10))
    # screen.blit(decrease_text, (decrease_button.x + 10, decrease_button.y + 10))
    
    # Display score and level
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = level_font.render(f"Level: {level}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - 150, 10))
    
    pygame.display.flip()
    pygame.time.delay(30)
    
    # Display the frame with hand landmarks using matplotlib
    ax.clear()
    ax.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.draw()
    plt.pause(0.001)

cap.release()
plt.close()
pygame.quit()
