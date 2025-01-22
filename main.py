from imaging import get_bounding_boxes
import pyautogui
import time
import json
import os
from PIL import ImageDraw, ImageFont, Image
time.sleep(5)
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
# Take a screenshot of the entire screen in real-time
screenshot = pyautogui.screenshot()
screenshot_path = "current_screen.png"
screenshot.save(screenshot_path)
from google import genai
# Initialize the client
client = genai.Client(api_key=GOOGLE_API_KEY)

# Get bounding boxes from the current screenshot
bb = get_bounding_boxes(screenshot_path, "Postman Icon")



# Extract the bounding box coordinates (already in screen coordinates)
bbox = bb["response"]["bbox"]
print(bbox)
x1, y1, x2, y2 = bbox

# Calculate the center of the bounding box
center_x = (x1 + x2) // 2
center_y = (y1 + y2) // 2

# Move the mouse to the center and click
pyautogui.moveTo(center_x, center_y)
pyautogui.click()

# Optional delay to observe the action
time.sleep(1)

# Load the screenshot image
image = Image.open(screenshot_path)

# Create a drawing context
draw = ImageDraw.Draw(image)

# Draw the bounding box on the image
draw.rectangle([x1, y1, x2, y2], outline="red", width=2)

# Optionally, draw the center point
draw.ellipse([center_x - 5, center_y - 5, center_x + 5, center_y + 5], fill="blue")

# Show the image with the bounding box
image.show()