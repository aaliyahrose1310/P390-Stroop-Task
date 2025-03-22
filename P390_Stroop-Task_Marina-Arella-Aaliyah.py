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

# Initialize pygame
pygame.init()