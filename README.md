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
# Aaliyah's Stroop copy

```python
import pygame
import random
import time
import os  # Where the data is going to be stored
import csv  # Where the data is going to be stored
import sys  # Needed for proper exit handling
import uuid # For unique file names
from datetime import datetime # For timestamped session names
import pandas as pd  # Import pandas for data handling
from scipy.stats import ttest_ind  # Import ttest_ind for statistical analysis

# Define session name to avoid overwriting files
session_name = f"session_{datetime.today().strftime('%Y%m%d')}_{str(uuid.uuid4())[:8]}"
save_folder = os.path.expanduser("~/Documents/StroopData")  # Adjust path if needed
os.makedirs(save_folder, exist_ok=True)  # Create folder if it doesn't exist

# Initialize pygame
pygame.init()

# Function to save results after every trial
def save_results_to_csv(results):
    """ Saves results to a uniquely named CSV file in the specified folder. """
    save_path = os.path.join(save_folder, f"stroop_results_{session_name}.csv")
    
    with open(save_path, "a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Write headers only if file is empty
            writer.writerow(["Trial Number", "Cue Side", "Word", "Response", "Reaction Time (ms)", "Correct"])
        writer.writerows(results)  # Save results
    print(f"Results saved to {save_path}")

def setup_screen():
    """ Sets up the screen dimensions and display settings. """
    WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Stroop Task")
    return screen, WIDTH, HEIGHT

def get_colors():
    """ Returns the color values dictionary for the Stroop Task. """
    return {
        "RED": (255, 0, 0),
        "BLUE": (0, 0, 255),
        "GREEN": (0, 255, 0),
        "YELLOW": (255, 255, 0)
    }

def get_center_position(text_surface, screen_width, screen_height):
    """ Returns the center position of the text surface on the screen. """
    return screen_width // 2 - text_surface.get_width() // 2, screen_height // 2 - text_surface.get_height() // 2

def get_font(size):
    """ Returns a font object of the specified size. """
    return pygame.font.Font(None, size)

def draw_text(screen, text, font, color, position):
    """ Draws text on the screen. """
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def get_cue_side():
    """ Randomly selects the cue side (left or right) for the trial. """
    return random.choice(["left", "right"])

def run_trial(screen, font, colors, width, height, trial_number, soa=500):
    """ Runs a single Stroop trial and records reaction time and responses. """
    # Select trial condition (stroop, control, or baseline)
    condition = random.choice(["stroop", "control", "baseline"])

# Select random word
    word = random.choice(list(colors.keys()))
    
    # Select random color for the target display
    target_color = random.choice(list(colors.values()))
    
# If the trial is a Stroop trial, ensure word and color do not match
    if condition == "stroop":
        while colors[word] == target_color:
            target_color = random.choice(list(colors.values()))

    # If the trial is a Control trial or Baseline trial, word and color must match
    if condition == "control" or condition == "baseline":
        target_color = colors[word]  # Word and color must match in control and baseline conditions

    # Create stimulus text
    text_surface = font.render(word, True, target_color)
    position = get_center_position(text_surface, width, height)

    # Show cue
    cue_side = get_cue_side()
    screen.fill((255, 255, 255))  # Clear screen
    draw_text(screen, cue_side, font, (0, 0, 0), position)
    pygame.display.flip()

    # Wait for the space key to proceed
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_key = False

    # Show target (stimulus)
    pygame.time.delay(soa)  # Wait for SOA (stimulus onset asynchrony)

    # Start timing for reaction
    start_time = time.time()

    # Wait for response from user
    response = None
    while response is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Red
                    response = "RED"
                elif event.key == pygame.K_g:  # Green
                    response = "GREEN"
                elif event.key == pygame.K_b:  # Blue
                    response = "BLUE"
                elif event.key == pygame.K_y:  # Yellow
                    response = "YELLOW"

    # Calculate reaction time
    reaction_time = (time.time() - start_time) * 1000  # In milliseconds

    # Check if the response was correct
    correct = response == target_color

    # Save results for this trial
    results = [[trial_number, cue_side, word, response, reaction_time, correct, condition]]
    save_results_to_csv(results)

    return reaction_time, correct, condition

def show_ending_screen(screen, font, width, height, total_trials, correct_trials, avg_reaction_time):
    """ Shows the final screen with performance statistics. """
    screen.fill((255, 255, 255))  # Clear screen
    messages = [
        "Task Complete!",
        f"Total Trials: {total_trials}",
        f"Correct Responses: {correct_trials}",
        f"Average Reaction Time: {avg_reaction_time:.2f} ms",
        "Press 'ESC' to Exit."
    ]

    y_pos = height // 4
    for line in messages:
        draw_text(screen, line, font, (0, 0, 0), (width // 2 - font.size(line)[0] // 2, y_pos))
        y_pos += 60
    
    pygame.display.flip()

    # Wait for user to press 'ESC' to quit
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    screen, width, height = setup_screen()
    colors = get_colors()
    font = get_font(96)
    
    num_trials = 50  # Number of trials
    results = []

    # Instruction screen
    instructions = [
        "Welcome to our Stroop Task Experiment. We appreciate your time and participation",
        "You will see colour names (red, blue, green, yellow) printed in different colours",
        "Your task is to respond with the color of the word, NOT the word itself.",
        "Press 'R' for Red, 'G' for Green, 'B' for Blue, 'Y' for Yellow.",
        "Press SPACE to begin the experiment"
    ]
    
    screen.fill((255, 255, 255))
    y_pos = height // 4
    for line in instructions:
        draw_text(screen, line, font, (0, 0, 0), (width // 2 - font.size(line)[0] // 2, y_pos))
        y_pos += 60
    pygame.display.flip()
    
    # Wait for space to start the task
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_key = False
    
    # Run the Stroop trials
    for trial in range(num_trials):
        reaction_time, correct, condition = run_trial(screen, font, colors, width, height, trial + 1)
        results.append([trial + 1, reaction_time, correct, condition])

    # After all trials, display results in terminal
    print("Experiment complete!")
    
    # Read CSV results into a Pandas DataFrame
    df = pd.read_csv(os.path.join(save_folder, f"stroop_results_{session_name}.csv"))
    print("Data summary:\n", df.describe())
    
    # Perform a T-test to compare reaction times for correct vs incorrect responses
    correct_rt = df['Reaction Time (ms)'][df['Correct'] == True]
    incorrect_rt = df['Reaction Time (ms)'][df['Correct'] == False]
    t_stat, p_value = ttest_ind(correct_rt, incorrect_rt)
    print("\nT-test results (Correct vs Incorrect RTs):")
    print(f"T-statistic: {t_stat}, P-value: {p_value}")

    # Exit pygame
    pygame.quit()

if __name__ == "__main__":
    main()
```
