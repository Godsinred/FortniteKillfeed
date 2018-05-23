import io
import os
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
import time

# credentials for vision.ImageAnnotatorClient() object
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/Users/godsinred/Desktop/GoogleAPI/account_key.json'
# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'Screenshot.png')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.text_detection(image=image)
labels = ''
try:
    labels = response.text_annotations[0].description.strip().split('\n')
except:
    print('here')

print("Lines:")
i = 1
for label in labels:
    print("Line " + str(i) + ": ", end='')
    print(label)
    i += 1