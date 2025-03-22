import pygame
import random
import time
import os  # Where the data is going to be stored
import csv  # Where the data is going to be stored
import sys  # Needed for proper exit handling
import uuid # For unique file names
from datetime import datetime # For timestamped session names

# Define session name to avoid overwriting files
session_name = f"session_{datetime.today().strftime('%Y%m%d')}_{str(uuid.uuid4())[:8]}"
save_folder = os.path.expanduser("~/Documents/StroopData")  # Adjust path if needed
os.makedirs(save_folder, exist_ok=True)  # Create folder if it doesn't exist

def save_results_to_csv(results):
    """ Saves results to a uniquely named CSV file in the specified folder. """
    save_path = os.path.join(save_folder, f"posner_results_{session_name}.csv")
    
    with open(save_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Cue Side", "Target Side", "Reaction Time", "Correct"])  # Added headers for clarity
        writer.writerows(results)  # Save results

    print(f"Results saved to {save_path}")

# Initialize pygame
pygame.init()

# Set to full screen to remove distractions
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Stroop Task")

