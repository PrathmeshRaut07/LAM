import pyautogui
import time

print("Press Ctrl+C to stop the coordinate tracker.")

try:
    while True:
        # Get the current mouse position
        x, y = pyautogui.position()
        
        # Print the coordinates
        print(f"X: {x}, Y: {y}", end="\r")  # \r to overwrite the previous line
        
        # Small delay to avoid flooding the console
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nCoordinate tracker stopped.")