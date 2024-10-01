import pyautogui
import time
from PIL import ImageGrab, ImageOps
import numpy as np

# Detection box coordinates for the obstacle region (based on the orange box)
dino_region = (435, 524, 874, 824)  # Top-left: (435, 524), Bottom-right: (874, 824)

# Function to capture the game screen and return the pixel values of the region
def capture_screen(region):
    image = ImageGrab.grab(bbox=region)
    gray_image = ImageOps.grayscale(image)  # Convert image to grayscale
    return np.array(gray_image)

# Function to detect obstacles by checking if any pixel values change in the box
def detect_obstacle(prev_screen_data, current_screen_data):
    # Compare current screen data with the previous one; detect movement if arrays differ
    difference = np.sum(current_screen_data - prev_screen_data)

    # If there is any significant movement (difference in pixel values), return True
    if difference > 1000:  # Adjust the threshold based on sensitivity required
        return True
    return False

# Function to handle jumping based on obstacle detection
def start_jumping():
    time.sleep(5)  # Wait 5 seconds to allow the user to switch to the game window

    # Capture the initial state of the screen region (to compare with future frames)
    prev_screen_data = capture_screen(dino_region)

    while True:
        # Capture the current state of the screen region
        current_screen_data = capture_screen(dino_region)

        # Check if there's an obstacle/movement detected
        if detect_obstacle(prev_screen_data, current_screen_data):
            pyautogui.press('space')  # Jump if movement is detected
            time.sleep(0.1)  # Prevent multiple jumps by pausing briefly

        # Update the previous screen data for the next comparison
        prev_screen_data = current_screen_data

        # Small delay to match the screen refresh rate and not overwhelm the CPU
        time.sleep(0.05)

# Start the function
start_jumping()
