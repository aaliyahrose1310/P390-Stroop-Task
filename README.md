# Marina's Stroop copy

```python
import pygame
import random
import time
import csv

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Full screen mode
pygame.display.set_caption("Stroop Test")

# Define colors
COLORS = {"RED": (255, 0, 0), "BLUE": (0, 0, 255), "GREEN": (0, 255, 0), "YELLOW": (255, 244, 79)}
COLOR_NAMES = list(COLORS.keys())
KEY_MAPPING = {pygame.K_z: "RED", pygame.K_x: "BLUE", pygame.K_n: "GREEN", pygame.K_m: "YELLOW"}

# Fonts
font = pygame.font.Font(None, 90)
intro_font = pygame.font.Font(None, 60)

# Function to display text
def draw_text(text, color, position, font):
    render = font.render(text, True, color)
    rect = render.get_rect(center=position) #centering the text in the middle
    screen.blit(render, rect)

# Show instructions
def show_instructions():
    steps = [
        "Welcome to the Stroop Test! (press SPACE to continue)",
        "Your task is to identify the COLOR of the word, not the word itself (press SPACE to continue)",
        "Press the corresponding key to the color: (press SPACE to continue)",
        "Z = Red, X = Blue, N = Green, M = Yellow (press SPACE to continue)",
        "Press SPACE to start the control trial."
    ]
    
    # Calculate the total height of the instructions to center them
    total_height = len(steps) * 50  # 50 pixels between each line
    start_y = (HEIGHT - total_height) // 2  # Start in the vertical center of the screen
    
    for step in steps:
        screen.fill((255, 255, 255))  # Clear screen
        draw_text(step, (0, 0, 0), (WIDTH // 2, start_y), intro_font)  # Centered horizontally and vertically
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False
        start_y += 50  # Space between line

    return True

# Control trial (where word and color match)
def control_trial():
    control_count = 10  # 10 control trials
    results = []
    
    for _ in range(control_count):
        word = random.choice(COLOR_NAMES)
        color = word  # Set word and color to be the same
        color_rgb = COLORS[color]
        
        screen.fill((255, 255, 255))
        draw_text(word, color_rgb, (WIDTH // 2, HEIGHT // 2), font)
        pygame.display.flip()
        
        # Start timing response
        start_time = time.time()
        response = None
        
        while response is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key in KEY_MAPPING:
                    response = KEY_MAPPING[event.key]
                    reaction_time = time.time() - start_time
                    correct = response == color
                    results.append((word, color, response, correct, reaction_time))
        
        pygame.time.delay(500)  # Pause for 0.5 second
        pygame.event.clear()  # Clear any keypresses from the previous trial

    return results

# Run experiment
def stroop_test():
    if not show_instructions():
        return
    
    # Run control trials first
    control_results = control_trial()
    
    # After control, show the instructions for the main Stroop test
    if control_results is not None:
        screen.fill((255, 255, 255))
        draw_text("The control portion is now complete.", (0, 0, 0), (WIDTH // 2, HEIGHT // 3), font)
        draw_text("Press SPACE to start the official Stroop test.", (0, 0, 0), (WIDTH // 2, HEIGHT // 2), intro_font)
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False

    # Now run the official Stroop test
    running = True
    trial_count = 10  # Number of trials
    results = []

    # Main Stroop Test Loop
    for _ in range(trial_count):
        word = random.choice(COLOR_NAMES)
        color = random.choice(COLOR_NAMES)
        color_rgb = COLORS[color]
        
        screen.fill((255, 255, 255))
        draw_text(word, color_rgb, (WIDTH // 2, HEIGHT // 2), font)
        pygame.display.flip()
        
        start_time = time.time()
        response = None
        
        while response is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key in KEY_MAPPING:
                    response = KEY_MAPPING[event.key]
                    reaction_time = time.time() - start_time
                    correct = response == color
                    results.append((word, color, response, correct, reaction_time))
        
        pygame.time.delay(500)  # Pause for 0.5 second
        pygame.event.clear()  # Clear any keypresses from the previous trial

    # Save results to CSV
    with open("stroop_results.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Word", "Color", "Response", "Correct", "Reaction Time (s)"])  # Header
        writer.writerows(results)  # Write all trial data

    print("Results saved to stroop_results.csv")
    pygame.quit()  # Quit Pygame AFTER saving results

# Run the Stroop test
stroop_test()
```
#Aaliyah's Stroop copy

```python

