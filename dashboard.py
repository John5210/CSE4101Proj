import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init() 

# Creating the pygame window
screen = pygame.display.set_mode((830, 830))
pygame.display.set_caption("Dashboard")

# Definine font and colors
font = pygame.font.Font(None, 36)
text_color = (255, 255, 255)
text = ""
# Loading steering wheel image
steering_wheel = pygame.image.load('steering_wheel.png').convert_alpha() 
steering_wheel_rect = steering_wheel.get_rect()
# Setting steering wheel angle to start at 0
rotation_angle = 2
rotation_speed = 2

# Getting wheel jpg dimensions
image_width, image_height = steering_wheel.get_width(), steering_wheel.get_height()

# Calculating center position
screen_width, screen_height = 830, 830
center_x = (screen_width - image_width) // 2
center_y = (screen_height - image_height) // 2

# Moving text to bottom left of screen setup
text_x = 10
text_y = screen_height - 40

# Updating the display
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    text = "Pressed Keys: "
    if keys[K_w] or keys[K_UP]:
        # Checking for forward movement
        text += "W "
        rotation_angle += 2 # Rotating wheel 
    if keys[K_s] or keys[K_DOWN]:
        # Checking for braking
        text += "S "

    if keys[K_a] or keys[K_LEFT]:
        # Checking for left movement
        text += "A "
        rotation_angle += rotation_speed
    elif keys[K_d] or keys[K_RIGHT]:
        # Checking for right movement
        text += "D "
        rotation_angle -= rotation_speed # Rotating wheel
    else:
        # Resetting wheel position when unpressed
        if rotation_angle > 0:
            rotation_angle = max(0, rotation_angle - rotation_speed)
        elif rotation_angle < 0:
            rotation_angle = min(0, rotation_angle + rotation_speed)

    # Clearing the screen
    screen.fill((0, 0, 0,)) # Fill with black background

    # Rotating wheel image
    rotated_steering_wheel = pygame.transform.rotate(steering_wheel, rotation_angle)
    rotated_steering_wheel_rect = rotated_steering_wheel.get_rect(center=steering_wheel_rect.center)
    
    # Render and display text & wheel
    screen.blit(rotated_steering_wheel, rotated_steering_wheel_rect)
    text_surface = font.render(text, True, text_color)
    screen.blit(text_surface, (text_x, text_y))

    pygame.display.update()
