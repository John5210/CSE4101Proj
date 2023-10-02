# accelarate => 'w'
# brakes => spacebar
# left indicator => left arrow
# right indicator => right arrow

import pygame
import sys
import math
from PyQt5.QtCore import QDateTime

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (800, 600)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FPS = 30

# Initialize the window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Car Dashboard")

# Initialize variables
speedometer_value = 0
accelerating = False
left_indicator_on = False
right_indicator_on = False
brake_lights_on = False
braking = False  # Flag to indicate if the brakes are applied

# Load images and resize them
arrow_left = pygame.image.load("arrow_left.png")  # Replace with your own image
arrow_left = pygame.transform.scale(arrow_left, (32, 32))  # Resize the image
arrow_right = pygame.image.load("arrow_right.png")  # Replace with your own image
arrow_right = pygame.transform.scale(arrow_right, (32, 32))  # Resize the image
brake_indicator = pygame.image.load("brake_indicator.png")
brake_indicator = pygame.transform.scale(brake_indicator, (32, 32))

# Create fonts
font = pygame.font.Font(None, 36)

# Initialize blinking variables
left_indicator_blinking = False
right_indicator_blinking = False
left_blink_start_time = 0
right_blink_start_time = 0
blink_duration = 500  # milliseconds (0.5 seconds)

normal_deceleration = 0.2  # Decrease speed by 0.5 km/h per frame
brake_deceleration = 0.5  # Decrease speed by 2.0 km/h per frame when braking

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                accelerating = True
            elif event.key == pygame.K_LEFT:
                if not left_indicator_blinking:
                    left_indicator_blinking = True  # Start blinking
                    left_blink_start_time = pygame.time.get_ticks()  # Record start time
                else:
                    left_indicator_blinking = False  # Stop blinking
            elif event.key == pygame.K_RIGHT:
                if not right_indicator_blinking:
                    right_indicator_blinking = True  # Start blinking
                    right_blink_start_time = pygame.time.get_ticks()  # Record start time
                else:
                    right_indicator_blinking = False  # Stop blinking
            elif event.key == pygame.K_SPACE:
                braking = True  # Start braking
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                accelerating = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                left_indicator_on = False
                right_indicator_on = False
            if event.key == pygame.K_SPACE:
                braking = False  # Stop braking

    # Update speedometer when accelerating
    if accelerating and speedometer_value < 200:
        speedometer_value += 1

    # Apply continuous braking when the spacebar is pressed
    if braking:
        if speedometer_value > 0:
            speedometer_value -= brake_deceleration
        else:
            speedometer_value = 0
    else:
        # Apply slower deceleration when not pressing the spacebar
        if speedometer_value > 0:
            speedometer_value -= normal_deceleration
        else:
            speedometer_value = 0

    # Clear the screen
    screen.fill(WHITE)

    # Draw speedometer markings
    for angle in range(-210, 31, 10):  # Markings from -150 degrees to 30 degrees
        angle_rad = math.radians(angle)
        x1 = 400 + 190 * math.cos(angle_rad)
        y1 = 300 + 190 * math.sin(angle_rad)
        x2 = 400 + 200 * math.cos(angle_rad)
        y2 = 300 + 200 * math.sin(angle_rad)
        pygame.draw.line(screen, RED, (x1, y1), (x2, y2), 4)

    # Calculate pointer angle based on speed
    pointer_angle = math.radians(210 - (speedometer_value / 200) * 240)
    pointer_length = 180

    # Calculate the endpoint of the pointer line
    pointer_x = 400 + pointer_length * math.cos(pointer_angle)
    pointer_y = 300 - pointer_length * math.sin(pointer_angle)

    pygame.draw.line(screen, RED, (400, 300), (pointer_x, pointer_y), 4)

    # Display speed as a whole number without decimal places
    speed_text = font.render(f"Speed: {int(speedometer_value)} mph", True, RED)
    real_time = font.render(QDateTime.currentDateTime().toString("hh:mm:ss"), True, RED)
    screen.blit(speed_text, (350, 50))
    screen.blit(real_time, (350, 20))

    # Handle left indicator blinking
    if left_indicator_blinking:
        current_time = pygame.time.get_ticks()
        if current_time - left_blink_start_time >= blink_duration:
            left_indicator_on = not left_indicator_on
            left_blink_start_time = current_time  # Reset the start time

    # Handle right indicator blinking
    if right_indicator_blinking:
        current_time = pygame.time.get_ticks()
        if current_time - right_blink_start_time >= blink_duration:
            right_indicator_on = not right_indicator_on
            right_blink_start_time = current_time  # Reset the start time

    # Draw left indicator (blinked if necessary)
    if left_indicator_on:
        screen.blit(arrow_left, (50, 50))

    # Draw right indicator (blinked if necessary)
    if right_indicator_on:
        screen.blit(arrow_right, (700, 50))

    # Draw brake lights
    if braking:
        screen.blit(brake_indicator, (380, 450))
        #pygame.draw.rect(screen, RED, (350, 500, 100, 50))

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
