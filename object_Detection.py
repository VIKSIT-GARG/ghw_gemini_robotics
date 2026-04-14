import os 
from dotenv import load_dotenv   
from google import genai
from google.genai import types 
import json 
from PIL import Image 


load_dotenv() 

# step 1 - fetch out geminiapikey 

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))          


#  loading image to prompt 

image_path = "image.png"
my_image = client.files.upload(file=image_path)

#step 3 - add a prompt 

prompt = "locate the bee plushie from the image and give me the bounding box coordinates in JSON format [ymin,xmin,ymax,xmax] and also inclue a label "

#step 4 - call the gemini robotics model - 

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

print(image_response.text)



#  step -5  parse the json respomse 

data = json.loads(image_response.text)

box = data[0]['box_2d']

print(f"Bounding box coordinates for the bee plushie: {box}"   )