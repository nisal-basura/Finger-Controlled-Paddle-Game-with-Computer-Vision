

# Finger-Controlled Paddle Game with Computer Vision


## Overview

This project is a fun and interactive game that uses computer vision to track hand gestures, allowing you to control a paddle and play a classic ball-and-paddle game. The game is built using Python, OpenCV, Mediapipe, and Pygame.

## Features

- **Hand Gesture Control**: Uses Mediapipe to detect hand landmarks and control the paddle.
- **Real-time Video Feed**: Integrates OpenCV video feed directly within the Pygame window.
- **Sound Effects and Music**: Includes background music and sound effects for an engaging experience.

## Technologies Used

- **Python**: Programming language.
- **OpenCV**: For capturing and processing video feed.
- **Mediapipe**: For hand gesture recognition.
- **Pygame**: For game development and handling game mechanics.

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/finger-controlled-paddle-game.git
   cd finger-controlled-paddle-game
   ```

2. **Install the required packages**:
   ```sh
   pip install opencv-python mediapipe pygame matplotlib
   ```

3. **Download the background music and sound effects**:
   - Place `background_music.mp3`, `hit_sound.wav`, and `wall_sound.wav` in the project directory.

## Usage

1. **Run the game**:
   ```sh
   python game.py
   ```

2. **Control the game**:
   - Use your hand to control the paddle. The game will detect your index finger and move the paddle accordingly.
   - Adjust the ball speed on the interactive dashboard by hovering your finger over the "Speed +" or "Speed -" buttons.
   - Start the game by hovering your finger over the "Start" button.

## Code Structure

- **game.py**: Main game logic and implementation.
- **background_music.mp3**: Background music file.
- **hit_sound.wav**: Sound effect for hitting the ball.
- **wall_sound.wav**: Sound effect for hitting the wall.

## How It Works

1. **Hand Detection**:
   - The game uses Mediapipe to detect hand landmarks in real-time.
   - The index finger tip position is used to control the paddle.

2. **Game Mechanics**:
   - The paddle moves horizontally based on the detected hand position.
   - The ball bounces off the paddle and walls, and the game keeps track of the score and level.
   - The ball speed increases as the player progresses through levels.

3. **Dashboard**:
   - An interactive dashboard allows the player to adjust the ball speed before starting the game.
   - The player can start the game by hovering their finger over the "Start" button.

