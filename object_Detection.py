import os 
from google import genai
from google.genai import types  

# step 1 - fetch out geminiapikey 

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))          


#  loading image to prompt 

image_path = "/home/byebye/Documents/MLH/robotics/robotics/image.png"
my_image = client.files.upload(file-image_path)