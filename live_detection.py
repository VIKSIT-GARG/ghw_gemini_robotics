import os 
from dotenv import load_dotenv   
from google import genai
from google.genai import types 
import json 
from PIL import Image, ImageDraw

import serial 
import cv2



load_dotenv() 

# Step 1: Fetch our Gemini API key and init our client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = """
Look at this frame. cell in it?
If yes, output the exact command: cell_detected 
If no, output the exact command: IDLE

Return ONLY a JSON object in this format:
{"command": "YOUR_COMMAND"}

"""


ARDUINO_COM = "/dev/ttyACM0"
BAUD_RATE = 9600 

arduino = serial.Serial(ARDUINO_COM, BAUD_RATE , timeout=1)

capture_Cam = cv2.VideoCapture(0)

while True:
    ret, frame = capture_Cam.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Save the captured frame as an image file
    cv2.imwrite("current_frame.jpg", frame)

    my_image = client.files.upload(file="current_frame.jpg")

    image_response = client.models.generate_content(
        model="gemini-robotics-er-1.5-preview",
        contents=[
            my_image,
            prompt
        ],
        config = types.GenerateContentConfig(
            temperature=0.5,
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )
    )

    result = json.loads(image_response.text)
    command = result.get("command", "IDLE")
    print(command)

    #send to arduino 
    # 
    arduino.write((command + '\n').encode('utf-8'))

capture_Cam.release()
arduino.close()  
