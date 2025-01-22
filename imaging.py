from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import json

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize the client
client = genai.Client(api_key=GOOGLE_API_KEY)

# Define system instructions and safety settings
# bounding_box_system_instructions = """
#     Return bounding boxe as a JSON array with label. Never return masks or code fencing. Give only one Bbox most probable Bbox according to prompt.
#     return json with key "response"
# """
bounding_box_system_instructions = """
    Return bounding boxes as a JSON array with labels. Never return masks or code fencing. Limit to 25 objects.
    If an object is present multiple times, name them according to their unique characteristic (colors, size, position, unique characteristics, etc..).
      """

safety_settings = [
    types.SafetySetting(
        category="HARM_CATEGORY_DANGEROUS_CONTENT",
        threshold="BLOCK_ONLY_HIGH",
    ),
]

def get_bounding_boxes(image_path, query, model_name="gemini-2.0-flash-thinking-exp-1219"):
    """
    Function to get bounding boxes from an image based on a query.

    Args:
        image_path (str): Path to the image file.
        query (str): The query to send to the model.
        model_name (str): The name of the model to use.

    Returns:
        dict: JSON object containing bounding boxes.
    """
    # Load and resize image
    im = Image.open(BytesIO(open(image_path, "rb").read()))
    im.thumbnail([1024, 1024], Image.Resampling.LANCZOS)

    # Run model to find bounding boxes
    response = client.models.generate_content(
        model=model_name,
        contents=[query, im],
        config=types.GenerateContentConfig(
            system_instruction=bounding_box_system_instructions,
            temperature=0.5,
            safety_settings=safety_settings,
        )
    )

    # Parse the response to extract JSON
    bounding_boxes = parse_json(response.text)
    return json.loads(bounding_boxes)

def parse_json(json_output):
    """
    Parses out the markdown fencing from the JSON output.

    Args:
        json_output (str): The JSON output from the model.

    Returns:
        str: Clean JSON string.
    """
    lines = json_output.splitlines()
    for i, line in enumerate(lines):
        if line == "```json":
            json_output = "\n".join(lines[i+1:])  # Remove everything before "```json"
            json_output = json_output.split("```")[0]  # Remove everything after the closing "```"
            break  # Exit the loop once "```json" is found
    return json_output

import json
from PIL import ImageColor,ImageFont,ImageDraw
additional_colors = [colorname for (colorname, colorcode) in ImageColor.colormap.items()]

def plot_bounding_boxes(im, bounding_boxes):
    """
    Plots bounding boxes on an image with markers for each a name, using PIL, normalized coordinates, and different colors.

    Args:
        img_path: The path to the image file.
        bounding_boxes: A list of bounding boxes containing the name of the object
         and their positions in normalized [y1 x1 y2 x2] format.
    """

    # Load the image
    img = im
    width, height = img.size
    print(img.size)
    # Create a drawing object
    draw = ImageDraw.Draw(img)

    # Define a list of colors
    colors = [
    'red',
    'green',
    'blue',
    'yellow',
    'orange',
    'pink',
    'purple',
    'brown',
    'gray',
    'beige',
    'turquoise',
    'cyan',
    'magenta',
    'lime',
    'navy',
    'maroon',
    'teal',
    'olive',
    'coral',
    'lavender',
    'violet',
    'gold',
    'silver',
    ] + additional_colors

    # Parsing out the markdown fencing
    bounding_boxes = parse_json(bounding_boxes)

    font = ImageFont.truetype("NotoSansCJK-Regular.ttc", size=14)

    # Iterate over the bounding boxes
    for i, bounding_box in enumerate(json.loads(bounding_boxes)):
      # Select a color from the list
      color = colors[i % len(colors)]

      # Convert normalized coordinates to absolute coordinates
      abs_y1 = int(bounding_box["box_2d"][0]/1000 * height)
      abs_x1 = int(bounding_box["box_2d"][1]/1000 * width)
      abs_y2 = int(bounding_box["box_2d"][2]/1000 * height)
      abs_x2 = int(bounding_box["box_2d"][3]/1000 * width)

      if abs_x1 > abs_x2:
        abs_x1, abs_x2 = abs_x2, abs_x1

      if abs_y1 > abs_y2:
        abs_y1, abs_y2 = abs_y2, abs_y1

      # Draw the bounding box
      draw.rectangle(
          ((abs_x1, abs_y1), (abs_x2, abs_y2)), outline=color, width=4
      )

      # Draw the text
      if "label" in bounding_box:
        draw.text((abs_x1 + 8, abs_y1 + 6), bounding_box["label"], fill=color, font=font)

    # Display the image
    img.show()
# Example usage
if __name__ == "__main__":
    image_path = "Screenshot 2025-01-22 163251.png"
    query = "Annoted annn the boxes"
    bounding_boxes = get_bounding_boxes(image_path, query)  # Assuming this returns a dictionary
    print(bounding_boxes)
    image=Image.open(image_path)
    plot_bounding_boxes(image,bounding_boxes)

    # # Extract the bounding box directly from the dictionary
    # bbox = bounding_boxes["response"]["bbox"]

    # # Print the bounding box
    # print("Bounding Box:", bbox)

   